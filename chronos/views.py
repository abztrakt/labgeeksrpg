from django.shortcuts import render_to_response, get_object_or_404
from labgeeksrpg.chronos.models import Shift 
from labgeeksrpg.player.models import Player

def report(request):
    shifts = Shift.objects.all()
    return render_to_response('report.html', locals())

def time(request):
    players = Player.objects.all()
    return render_to_response('time.html', locals())
