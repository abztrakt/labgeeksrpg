# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from labgeeksrpg.player.models import Player

def list(request):
    players = Player.objects.all()
    return render_to_response('list.html', locals())

def detail(request, player):
    debug = dir(Player.objects)
    #debug = Player.objects.get()
    p = get_object_or_404(Player, uwnetid=player)
    return render_to_response('detail.html', locals())
