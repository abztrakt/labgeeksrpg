from django.shortcuts import render_to_response, HttpResponseRedirect
from labgeeksrpg.forms import LoginForm
from django.contrib.auth import authenticate, login


def labgeeks_login(request):
    if request.method == 'POST': 
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    #return HttpResponseRedirect('/success/')
                    # Redirect to the success page
                else:
                    return HttpResponseRedirect('/inactive/')
                    # Return a disabled account error
            else:
                return HttpResponseRedirect('/invalid_login/')
                #Return an invalid login error
    else:
        form = LoginForm()

    return render_to_response('login.html', locals())

def success(request):
    return render_to_response('success.html')
