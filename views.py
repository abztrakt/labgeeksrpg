from django.shortcuts import render_to_response, HttpResponseRedirect
from labgeeksrpg.forms import LoginForm
from django.contrib.auth import authenticate, login


def labgeeks_login(request):
    """ Login a user. Called by the @login_required decorator.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(request.GET['next'])
    elif request.method == 'POST': 
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(request.GET['next'])
                else:
                    # Return a disabled account error
                    return HttpResponseRedirect('/inactive/')
    else:
        form = LoginForm()

    return render_to_response('login.html', locals())

def inactive(request):
    """ Return if a user's account has been disabled.
    """
    return render_to_response('inactive.html')

def success(request):
    """ If the user just logs in, we should redirect them to this view unless there is a 'next' GET var.
    """
    return render_to_response('login_success.html')
