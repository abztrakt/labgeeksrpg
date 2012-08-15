from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404, \
    HttpResponseRedirect
from django.template import RequestContext
from labgeeksrpg.chronos.forms import ShiftForm
from labgeeksrpg.chronos.models import Shift, Punchclock

from labgeeksrpg.utils import ReportCalendar, TimesheetCalendar
from django.contrib.auth.models import User
from datetime import date
from django.utils.safestring import mark_safe

from people.models import UserProfile


def list_options(request):
    """ Lists the options that users can get to when using chronos.
    """
    return render_to_response('options.html', locals())


def get_shifts(year, month, day=None, user=None, week=None, payperiod=None):
    """ This method is used to return specific shifts
        Since the calendar model is used, year and month both need to be given
        The day, user, week, and payperiod parameters are optional and only used for detailed shifts.
    """
    if day and user:
        # We are grabing a specific user's day shift.
        shifts = Shift.objects.filter(intime__year=int(year), intime__month=int(month), intime__day=int(day), person=user)
    elif day:
        # We are grabing total shifts in a day
        shifts = Shift.objects.filter(intime__year=int(year), intime__month=int(month), intime__day=int(day))
    elif user:
        # We are grabing all of the user's shift in the given month and year
        shifts = Shift.objects.filter(intime__year=int(year), intime__month=int(month), person=user)
    else:
        # We are grabing all of the total shifts in the given month and year.
        shifts = Shift.objects.filter(intime__year=int(year), intime__month=int(month))

    if week:
        #Filter the shifts by the given week of the month (i.e. week=1 means grab shifts in 1st week of month)
        first_week = date(int(year), int(month), 1).isocalendar()[1]

        #TODO: fix this hack to get around isocaledar's first week of the year wierdness. See #98
        if first_week == 52 and int(month) == 1:
            first_week = 1

        weekly = {}
        for shift in shifts:
            shift_date = shift.intime
            this_week = shift_date.isocalendar()[1]
            if this_week == 52 and int(month) == 1:
                this_week = 1
            week_number = this_week - first_week + 1
            if week_number in weekly:
                weekly[week_number].append(shift)
            else:
                weekly[week_number] = [shift]
        shifts = weekly[int(week)]
    elif payperiod:
        #Filter the shifts by the given payperiod of the month (i.e. payperiod=1 means grab shifts in 1st payperiod of month)
        payperiod_shifts = {'first': [], 'second': []}
        for shift in shifts:
            shift_date = shift.intime
            if shift_date.day <= 15:
                payperiod_shifts['first'].append(shift)
            else:
                payperiod_shifts['second'].append(shift)

        if int(payperiod) == 1:
            shifts = payperiod_shifts['first']
        else:
            shifts = payperiod_shifts['second']

    #Return the correct shifts
    return shifts


def calc_shift_stats(shifts, year, month):
    '''
    This method returns various calculations regarding a collection of shifts in a given year and month.
    '''
    payperiod_totals = {'first': 0, 'second': 0}
    weekly = {}
    first_week = date(year, month, 1).isocalendar()[1]

    #TODO: fix this hack around isocalendars calculating first week of the year, see #98
    if first_week == 52 and month == 1:
        first_week = 1

    for shift in shifts:
        week_number = shift.intime.isocalendar()[1] - first_week + 1

        if week_number not in weekly:
            weekly[week_number] = 0

        if shift.outtime:
            shift_date = shift.intime
            length = float(shift.length())

            #Keep track of pay period totals
            if shift_date.day <= 15:
                #1st pay period
                payperiod_totals['first'] += length
            else:
                #2nd pay period
                payperiod_totals['second'] += length

            weekly[week_number] += length

    #Sort the weekly totals
    weeks = weekly.keys()
    weeks.sort()
    weekly_totals = []
    for i in range(0, len(weeks)):
        weekly_totals.append({'week': weeks[i], 'total': weekly[weeks[i]]})

    result = {
        'weeks': weeks,
        'weekly_totals': weekly_totals,
        'payperiod_totals': payperiod_totals,
    }

    return result


def prev_and_next_dates(year, month):
    '''
    This method returns a previous and upcomming months from a given month and year.
    '''
    #Figure out the prev and next months
    if month == 1:
        #Its January
        prev_date = date(year - 1, 12, 1)
        next_date = date(year, 2, 1)
    elif month == 12:
        #Its December
        prev_date = date(year, 11, 1)
        next_date = date(year + 1, 1, 1)
    else:
        #Its a regular month
        prev_date = date(year, month - 1, 1)
        next_date = date(year, month + 1, 1)

    result = {'prev_date': prev_date, 'next_date': next_date}
    return result
"""
    The methods and views below deal with OVERALL calendar information
"""


@login_required
def staff_report(request, year, month, day=None, user=None, week=None, payperiod=None):
    '''
    This view is used to display all shifts in a time frame. Only users with specific permissions can view this information.
    '''

    if not request.user.is_staff:
        message = 'Permission Denied'
        reason = 'You do not have permission to visit this part of the page.'

        return render_to_response('fail.html', locals())
    return specific_report(request, user, year, month, day, week, payperiod)


@login_required
def specific_report(request, user, year, month, day=None, week=None, payperiod=None):
    """ This view is used when viewing specific shifts in the given day. (Table form)
    """
    #Grab shifts
    if user:
        user = User.objects.get(username=user)

    all_shifts = get_shifts(year, month, day, user, week, payperiod)
    if day:
        description = "Viewing shifts for %s." % (date(int(year), int(month), int(day)).strftime("%B %d, %Y"))
    elif week:
        description = "Viewing shifts in week %d of %s." % (int(week), date(int(year), int(month), 1).strftime("%B, %Y"))
    else:
        #This should be a payperiod view
        description = "Viewing shifts in payperiod %d of %s." % (int(payperiod), date(int(year), int(month), 1).strftime("%B, %Y"))

    # The following code is used for displaying the user's call_me_by or first name.
    shifts = []
    for shift in all_shifts:
        if "\n\n" in shift.shiftnote:
            shiftnotes = shift.shiftnote.split("\n\n")
            shift.shiftinnote = shiftnotes[0]
            shift.shiftoutnote = shiftnotes[1]
        else:
            shift.shiftinnote = shift.shiftnote
            shift.shiftoutnote = ""

        user = User.objects.get(username=shift.person)
        try:
            profile = UserProfile.objects.get(user=user)

            if profile.call_me_by:
                user = profile.call_me_by
            else:
                user = user.first_name
        except UserProfile.DoesNotExist:
            user = user.first_name

        #Splits up shiftnotes into two separate variables if there are two to begin with
        if "\n\n" in shift.shiftnote:
            shiftnotes = shift.shiftnote.split("\n\n")
            shift.shiftinnote = shiftnotes[0]
            shift.shiftoutnote = shiftnotes[1]
        else:
            shift.shiftinnote = shift.shiftnote
            shift.shiftoutnote = ""

        data = {
            'person': user,
            'location': shift.in_clock.location,
            'intime': shift.intime,
            'outtime': shift.outtime,
            'length': shift.length,
            'shiftinnote': shift.shiftinnote,
            'shiftoutnote': shift.shiftoutnote,
        }
        shifts.append(data)

    return render_to_response('specific_report.html', locals())


@login_required
def report(request, user=None, year=None, month=None):
    """ Creates a report of shifts in the year and month.
    """

    if not request.user.is_staff:
        message = 'Permission Denied'
        reason = 'You do not have permission to visit this part of the page.'

        return render_to_response('fail.html', locals())

    # Initiate the return argument list
    args = {}

    # Grab shifts
    if not year:
        year = date.today().year
    if not month:
        month = date.today().month
    year = int(year)
    month = int(month)
    shifts = get_shifts(year, month, None, user)

    # Calculate the previous and upcomming months.
    prev_and_next = prev_and_next_dates(year, month)
    prev_date = prev_and_next['prev_date']
    next_date = prev_and_next['next_date']

    # Create calendar and compute stats
    calendar = mark_safe(ReportCalendar(shifts, user=user).formatmonth(year, month))
    stats = calc_shift_stats(shifts, year, month)
    weeks = stats['weeks']

    args = {
        'request': request,
        'year': year,
        'month': month,
        'calendar': calendar,
        'prev_date': prev_date,
        'next_date': next_date,
        'weeks': weeks,
    }

    return render_to_response('report.html', args)


@login_required
def personal_report(request, user=None, year=None, month=None):
    """ Creates a personal report of all shifts for that user.
    """
    args = {}
    # Determine who the user is. This will return a calendar specific to that person.
    if not user:
        user = request.user
    else:
        user = User.objects.get(username=user)

    # If the year and month are not given, assume it is the current year & month.
    if not year:
        year = date.today().year
    if not month:
        month = date.today().month
    year = int(year)
    month = int(month)

    if request.user.is_authenticated():
        #Grab user's shifts
        shifts = get_shifts(year, month, None, user)
        calendar = mark_safe(TimesheetCalendar(shifts, user=user).formatmonth(year, month))
    else:
        shifts = None
        calendar = None

    # Calculate the previous and upcomming months.
    prev_and_next = prev_and_next_dates(year, month)
    prev_date = prev_and_next['prev_date']
    next_date = prev_and_next['next_date']

    #Compute shift stats
    stats = calc_shift_stats(shifts, year, month)
    payperiod_totals = stats['payperiod_totals']
    weekly_totals = stats['weekly_totals']

    args = {
        'request': request,
        'user': user.username,
        'year': year,
        'month': month,
        'calendar': calendar,
        'prev_date': prev_date,
        'next_date': next_date,
        'weekly_totals': weekly_totals,
        'payperiod_totals': payperiod_totals,
    }

    return render_to_response('options.html', args)


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
                # Setting the success variable that users will see on success page
                success = "OUT"
                at_time = oldshift.outtime
                at_time = at_time.strftime('%Y-%m-%d, %I:%M %p').replace(' 0', ' ')  # get rid of zeros on the hour

            else:
                # if shift.person  location.active_staff
                if this_shift.intime is None:
                    this_shift.intime = datetime.now()
                this_shift.in_clock = punchclock
                # On success, save the shift
                this_shift.save()
                # After successful shift save, add person to active_staff in appropriate Location
                location.active_users.add(this_shift.person)

                # Setting the success variable that users will see on the success page
                success = "IN"
                at_time = this_shift.intime
                at_time = at_time.strftime('%Y-%m-%d, %I:%M %p').replace(' 0', ' ')  # get rid of zeros on the hour

            return HttpResponseRedirect("success/?success=%s&at_time=%s&location=%s&user=%s" % (success, at_time, location, this_shift.person))

    #If POST is false, then return a new fresh form.
    else:
        form = ShiftForm()
        in_or_out = 'IN'
        if user in location.active_users.all():
            in_or_out = 'OUT'

    # The following code is used for displaying the user's call_me_by or first name.
    user = User.objects.get(username=user)
    try:
        profile = UserProfile.objects.get(user=user)
        if profile.call_me_by:
            user = profile.call_me_by
        else:
            user = user.first_name
    except UserProfile.DoesNotExist:
        user = user.first_name

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

    # The following code is used for displaying the user's call_me_by or first name.
    user = User.objects.get(username=user)
    try:
        profile = UserProfile.objects.get(user=user)
        if profile.call_me_by:
            user = profile.call_me_by
        else:
            user = user.first_name
    except UserProfile.DoesNotExist:
        user = user.first_name

    return render_to_response('success.html', locals())
