from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect
from datetime import datetime
from labgeeksrpg.chronos.forms import ShiftForm
from labgeeksrpg.chronos.models import Shift
from django.contrib.auth.decorators import login_required

@login_required
def report(request):
    shifts = Shift.objects.all()
    return render_to_response('report.html', locals())

@login_required
def time(request):
    #Check for POST, if not blank form, if true 'take in data'
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        #Check form data for validity, if not valid, fail gracefully
        if form.is_valid():
            #We are creating a shift object that we can manipulate programatically later
            this_shift = form.save(commit=False)
            this_shift.person = request.user
            #Getting machine location user is currently using
            punchclock = this_shift.punchclock
            location = punchclock.location
            #Check whether user has open shift at this location
            if this_shift.person in location.active_users.all():
                print "User is alreday here!"
                try:
                    oldshift = Shift.objects.filter(person=request.user, punchclock=location, outtime=None)
                    #import pdb; pdb.set_trace()
                    oldshift = oldshift[0]
                    oldshift.outtime = datetime.now()
                    oldshift.save()
                    location.active_users.remove(request.user)
                    #Setting the success variable that users will see on success page
                    success = "signed *OUT*"
                    at_time = oldshift.outtime
                except:
                    print "There was an error getting old shifts"
            
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
                success = "signed *IN*"
                at_time = this_shift.intime

            return HttpResponseRedirect("success/?success=%s&at_time=%s&location=%s&user=%s" % (success, at_time, location, this_shift.person))

    #If POST is false, then return a new fresh form.
    else:
        form = ShiftForm()

    user = request.user
    return render_to_response('time.html', locals())

def success(request):
    success = request.GET['success']
    at_time = request.GET['at_time']
    location = request.GET['location']
    user = request.GET['user']
    return render_to_response('success.html', locals())
