from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

def list_all(request):
    return render_to_response('list.html')

@login_required
def view_profile(request, name):
    profile = request.user.get_profile()

    return render_to_response('profile.html', locals())
