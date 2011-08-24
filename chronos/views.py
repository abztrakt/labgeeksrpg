from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404, \
    HttpResponseRedirect
from django.template import RequestContext
from labgeeksrpg.chronos.forms import ShiftForm
from labgeeksrpg.chronos.models import Shift, Punchclock

from labgeeksrpg.people.views import TimesheetCalendar
from datetime import date
from django.utils.safestring import mark_safe

def list_options(request):
    """ Lists the options that users can get to when using chronos.
    """
    return render_to_response('options.html', locals())

class ReportCalendar(TimesheetCalendar):
    """ This class is used for displaying the reports in a monthly calendar format.
        Overrides the TimesheetCalendar class by injecting the ability to view shifts of a the given day.
    """

    def formatday(self,day,weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if day <= 15:
                cssclass += ' first'
            else:
                cssclass += ' second'
            s = '<strong>%s</strong>' % (day)
            if date.today() == date(self.year,self.month,day):
                cssclass += ' today'
            if day in self.shifts:
                if not self.personal:
                    s += '<p><a href="/chronos/report/%s/%s/%s">Shift Details</a></p>' % (self.year,self.month,day)
                else:
                    s += '<p><a href="/chronos/report/personal/%s/%s/%s">Shift Details</a></p>' % (self.year,self.month,day)
                return super(ReportCalendar,self).day_cell(cssclass,s)
            return super(ReportCalendar,self).day_cell(cssclass,s)
        return super(ReportCalendar,self).day_cell('noday','&nbsp;')

def get_shifts(request,year,month,day=None,user=None):
    """ This method is used to return specific shifts
        Since the calendar model is used, year and month both need to be given
        The day and user parameters are optional and only used for detailed shifts.
    """
    if day and user:
        # We are grabing a specific user's day shift.
        shifts = Shift.objects.filter(intime__year=int(year), intime__month=int(month),intime__day=int(day), person = user)
    elif day:
        # We are grabing total shifts in a day
        shifts = Shift.objects.filter(intime__year=int(year), intime__month=int(month),intime__day=int(day))
    elif user:
        # We are grabing all of the user's shift in the given month and year
        shifts = Shift.objects.filter(intime__year=int(year), intime__month=int(month),person = user)
    else:
        # We are grabing all of the total shifts in the given month and year.
        shifts = Shift.objects.filter(intime__year=int(year), intime__month=int(month))

    #Return the correct shift
    return shifts

def get_calendar(target_date, shifts):
    """ This method is used to return a calendar formed from the given date and shifts.
    """

    args={}
    year = target_date.year
    month = target_date.month

    #Figure out the prev and next months
    if target_date.month == 1:
        #Its January
        args['prev_date'] = date(year-1,12,1)
        args['next_date'] = date(year, 2,1)
    elif target_date.month == 12:
        #Its December
        args['prev_date'] = date(year, 11,1)
        args['next_date'] = date(year+1,1,1)
    else:
        #Its a regular month
        args['prev_date'] = date(year,month-1,1)
        args['next_date'] = date(year,month+1,1)

    #Create calendar.
    args['calendar'] = mark_safe(ReportCalendar(shifts).formatmonth(year,month))

    #Return the arguments
    return args

"""
    The methods and views below deal with OVERALL calendar information
"""
@login_required
def specific_report(request,year,month,day):
    """ This view is used when viewing specific shifts in the given day. (Table form)
    """
    #Grab shifts
    shifts = get_shifts(request,year,month,day)

    #Send in the date
    spec_date = date(int(year),int(month),int(day))

    return render_to_response('specific_report.html',locals())

@login_required
def monthly_report(request,year,month):
    """ Creates a view of all shifts in a specific year and month in a calendar format.
    """
    return report(request,date(int(year),int(month),1))

@login_required
def report(request,target_date=date.today()):
    """ Creates a report of shifts in the year and month.
    """

    # Grab shifts
    shifts = get_shifts(request,target_date.year,target_date.month)
    
    # Create calendar and calendar related items (such as next_date).
    args = get_calendar(target_date, shifts)

    args['shifts'] = shifts 
    return render_to_response('report.html', args)

"""
    The methods and views below deal with PERSONAL calendar information.
"""
def monthly_personal_report(request, year,month):
    """ Creates a view of all shifts in a specific year and month for the user in a calendar format.
    """
    return personal_report(request,year,month)

def personal_report(request, year=date.today().year,month=date.today().month):
    """ Creates a personal report of all shifts for that user.
    """
    args = {}
    if request.user.is_authenticated():
        #Grab user's shifts 
        shifts = get_shifts(request,year,month,None,request.user)

        #Create calendar
        args = get_calendar(date(int(year),int(month),1),shifts)
        args['shifts'] = shifts
    else:
        args['shifts'] = [] 
    return render_to_response('options.html', args)

@login_required
def personal_report_specific(request,year,month,day):
    """ Creates a specific daily report for the user
    """
    shifts = get_shifts(request,year,month,day,request.user)
    spec_date = spec_date = date(int(year),int(month),int(day))
    return render_to_response('specific_report.html',locals())

@login_required
def time(request):
    """ Sign in or sign out of a shift.
    """
    #Generate a token to protect from cross-site request forgery
    c = {}
    c.update(csrf(request))
    
    # Grab information we want to pass along no matter what state we're in
    user = request.user
    #Getting machine location user is currently using
    current_ip = request.META['REMOTE_ADDR']

    try: 
        punchclock = Punchclock.objects.filter(ip_address=current_ip)[0]
    except:
        #implement bad monkey page redirect
        message = "You are a very bad monkey!"
        reason = "This computer isn't one of the punchclocks, silly..."
        log_msg = "Your IP Address, %s, has been logged and will be reported. (Just kidding. But seriously, you can't sign in or out from here.)" % current_ip
        return HttpResponseRedirect("fail/?message=%s&reason=%s&log_msg=%s" % (message, reason, log_msg))

    location = punchclock.location

    #Check for POST, if not blank form, if true 'take in data'
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        #Check form data for validity, if not valid, fail gracefully
        if form.is_valid():
            #We are creating a shift object that we can manipulate programatically later
            this_shift = form.save(commit=False)
            this_shift.person = request.user
            
            #Check whether user has open shift at this location
            if this_shift.person in location.active_users.all():
                try:
                    oldshift = Shift.objects.filter(person=request.user, outtime=None)
                    oldshift = oldshift[0]
                except IndexError:
                    reason = "Whoa. Something wacky is up. You appear to be signed in at %s, but don't have an open entry in my database. This is kind of a metaphysical crisis for me, I'm no longer sure what it all means." % location
                    return HttpResponseRedirect("fail/?reason=%s" % reason)
                oldshift.outtime = datetime.now()
                oldshift.shiftnote = "IN: %s\n\nOUT: %s" % (oldshift.shiftnote, form.data['shiftnote'])
                oldshift.out_clock = punchclock
                oldshift.save()
                location.active_users.remove(request.user)
                #Setting the success variable that users will see on success page
                success = "OUT"
                at_time = oldshift.outtime
                at_time = at_time.strftime('%Y-%m-%d, %I:%M %p').replace(' 0', ' ') #get rid of zeros on the hour
            
            else:
                #if shift.person  location.active_staff
                if this_shift.intime == None:
                    this_shift.intime = datetime.now()
                this_shift.in_clock = punchclock
                #On success, save the shift
                this_shift.save()
                #After successful shift save, add person to active_staff in appropriate Location
                location.active_users.add(this_shift.person)
            
                #Setting the success variable that users will see on the success page
                success = "IN"
                at_time = this_shift.intime
                at_time = at_time.strftime('%Y-%m-%d, %I:%M %p').replace(' 0', ' ') #get rid of zeros on the hour
                
            return HttpResponseRedirect("success/?success=%s&at_time=%s&location=%s&user=%s" % (success, at_time, location, this_shift.person))

    #If POST is false, then return a new fresh form.
    else:
        form = ShiftForm()
        in_or_out = 'IN'
        if user in location.active_users.all():
            in_or_out = 'OUT'
    return render_to_response('time.html', locals(), context_instance=RequestContext(request))

def fail(request):
    """ If signing in or out of a shift fails, show the user a page stating that. This is the page shown if someone tries to log in from a non-punchclock.
    """
    try:
        message = request.GET['message']
    except:
        pass
    try:
        reason = request.GET['reason']
    except:
        pass
    try:
        log_msg = request.GET['log_msg']
    except:
        pass
    return render_to_response('fail.html', locals())

def success(request):
    """ Show a page telling the user what they just successfully did.
    """
    success = request.GET['success']
    at_time = request.GET['at_time']
    location = request.GET['location']
    user = request.GET['user']
    return render_to_response('success.html', locals())
