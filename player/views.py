# Create your views here.

from django.shortcuts import render_to_response
from labgeeksrpg.player.models import Player

def list(request):
    players = Player.objects.all()
    return render_to_response('player/list.html', locals())
