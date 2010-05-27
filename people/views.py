from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def list_all(request):
    """ List all users in the system.
    """
    users = User.objects.all()
    return render_to_response('list.html', locals())

@login_required
def view_profile(request, name):
    """ Show a user profile.
    """
    profile = request.user.get_profile()

    return render_to_response('profile.html', locals())
