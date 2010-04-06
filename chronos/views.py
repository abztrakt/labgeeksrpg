from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect
from labgeeksrpg.chronos.forms import ShiftForm
from labgeeksrpg.player.models import Player

def report(request):
    shifts = Shift.objects.all()
    return render_to_response('report.html', locals())

def time(request):
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            shift = form.save(commit=True)
            return HttpResponseRedirect('something/')
    else:
        form = ShiftForm()

    return render_to_response('time.html', locals())
