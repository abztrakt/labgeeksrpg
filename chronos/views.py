from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect
from datetime import datetime
from labgeeksrpg.chronos.forms import ShiftForm
from labgeeksrpg.chronos.models import Shift
from labgeeksrpg.player.models import Player
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
            shift = form.save(commit=False)
            shift.person = request.user
            #Getting machine location user is currently using
            punchclock = shift.punchclock
            location = punchclock.location
            import pdb; pdb.set_trace()
            #Check whether user has open shift at this location
            #if shift.person  location.active_staff
            if shift.intime == None:
                shift.intime = datetime.now()
            #On success, save the shift
            shift.save()
            #After successful shift save, add person to active_staff in appropriate Location
            active = Player.objects.get(uwnetid=request.user.username)
            location.active_staff.add(active)
            return HttpResponseRedirect('success/')
    else:
        form = ShiftForm()

    user = request.user
    return render_to_response('time.html', locals())

def success(request):
    return render_to_response('success.html')
