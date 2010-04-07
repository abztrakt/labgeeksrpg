from django.shortcuts import render_to_response, get_object_or_404
from labgeeksrpg.player.models import Player

def list(request):
    """ List all of the people in the system.
    """
    players = Player.objects.all()
    return render_to_response('list.html', locals())

def detail(request, player):
    """ Show the user profile for a player.
    """
    debug = dir(Player.objects)
    #debug = Player.objects.get()
    p = get_object_or_404(Player, uwnetid=player)
    return render_to_response('detail.html', locals())
