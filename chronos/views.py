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
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            shift = form.save(commit=False)
            shift.person = request.user
            if shift.intime == None:
                shift.intime = datetime.now()
            #On success, save the shift
            shift.save()
            #After successful shift save, add person to active_staff in appropriate Location
            punchclock = shift.punchclock
            location = punchclock.location
            active = request.user
            location.active_users.add(active)
            return HttpResponseRedirect('success/')
    else:
        form = ShiftForm()

    user = request.user
    return render_to_response('time.html', locals())

def success(request):
    return render_to_response('success.html')
