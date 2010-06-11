from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404, \
    HttpResponseRedirect
from django.template import RequestContext
from labgeeksrpg.chronos.forms import ShiftForm
from labgeeksrpg.chronos.models import Shift, Punchclock

def list_options(request):
    """ Lists the options that users can get to when using chronos.
    """
    return render_to_response('options.html', locals())

@login_required
def report(request):
    """ Creates a report of all shifts in the history.
    """
    shifts = Shift.objects.all()
    return render_to_response('report.html', locals())

@login_required
def time(request):
    """ Sign in or sign out of a shift.
    """
    #Generate a token to protect from cross-site request forgery
    c = {}
    c.update(csrf(request))
    #Check for POST, if not blank form, if true 'take in data'
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        #Check form data for validity, if not valid, fail gracefully
        if form.is_valid():
            #We are creating a shift object that we can manipulate programatically later
            this_shift = form.save(commit=False)
            this_shift.person = request.user
            #Getting machine location user is currently using
            current_ip = request.META['REMOTE_ADDR']
            
            try: 
                this_shift.punchclock = Punchclock.objects.filter(ip_address=current_ip)[0]
            except:
                #implement bad monkey page redirect
                message = "You are a very bad monkey!"
                reason = "This computer isn't one of the punchclocks, silly..."
                log_msg = "Your IP Address, %s, has been logged and will be reported. (Just kidding. But seriously, you can't sign in or out from here.)" % current_ip
                return HttpResponseRedirect("fail/?message=%s&reason=%s&log_msg=%s" % (message, reason, log_msg))

            punchclock = this_shift.punchclock
            location = punchclock.location
            
            #Check whether user has open shift at this location
            if this_shift.person in location.active_users.all():
                try:
                    oldshift = Shift.objects.filter(person=request.user, outtime=None)
                    oldshift = oldshift[0]
                except IndexError:
                    reason = "Whoa. Something wacky is up. You appear to be signed in at %s, but don't have an open entry in my database. This is kind of a metaphysical crisis for me, I'm no longer sure what it all means." % location
                    return HttpResponseRedirect("fail/?reason=%s" % reason)
                oldshift.outtime = datetime.now()
                oldshift.save()
                location.active_users.remove(request.user)
                #Setting the success variable that users will see on success page
                success = "OUT"
                at_time = oldshift.outtime
                at_time = at_time.strftime('%Y-%m-%d, %I:%M %p').replace(' 0', ' ') #get rid of zeros on the hour
            
            else:
                #import pdb; pdb.set_trace()
                #if shift.person  location.active_staff
                if this_shift.intime == None:
                    this_shift.intime = datetime.now()
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
    user = request.user
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
