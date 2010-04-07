from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect
from datetime import datetime
from labgeeksrpg.chronos.forms import ShiftForm
from labgeeksrpg.chronos.models import Shift
from labgeeksrpg.player.models import Player
from django.contrib.auth.decorators import login_required

@login_required
def report(request):
    """ Create a report of all of the shifts logged in the database.
    """
    shifts = Shift.objects.all()
    return render_to_response('report.html', locals())

@login_required
def time(request):
    """ Clock in / clock out for a shift.
    """
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            shift = form.save(commit=False)
            shift.person = request.user
            if shift.intime == None:
                shift.intime = datetime.now()
            shift.save()
            return HttpResponseRedirect('success/')
    else:
        form = ShiftForm()

    user = request.user
    return render_to_response('time.html', locals())

def success(request):
    """ Show the user a success page after clocking in or out.
    """
    return render_to_response('success.html')
