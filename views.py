from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from labgeeksrpg.forms import LoginForm
import datetime
from labgeeksrpg.labgeeksrpg_config.models import Notification
from labgeeksrpg.labgeeksrpg_config.forms import NotificationForm


def hello(request):
    """ The root view of the site. Just static for now, but later we can return useful information for logged in users.
    Created a dashboard page.
    """
    #when a user is logged-in correctly
    if request.user.is_authenticated():
        locations = request.user.location_set.all()
        shifts = request.user.shift_set.all()
        clockin_time = 0
        if locations:
            clockin_time = shifts[len(shifts) - 1].intime

        notifications = Notification.objects.all()
        now = datetime.datetime.now()
        events = []
        alerts = []
        for noti in notifications:
            if noti.due_date:
                if now.date() - noti.due_date.date() >= datetime.timedelta(days=1):
                    noti.delete()
                elif not noti.due_date - now > datetime.timedelta(days=5):
                    events.append(noti)
            else:
                if (noti.date.year == now.year and noti.date.month == now.month and noti.date.day == now.day):
                    alerts.append(noti)
                else:
                    noti.delete()
        events.sort(key=lambda x: x.due_date)

        c = {}
        c.update(csrf(request))

        can_Add = False
        if request.user.has_perm('labgeeksrpg_config.add_notification'):
            can_Add = True

        if request.method == 'POST':
            form = NotificationForm(request.POST)
            if form.is_valid():
                notification = form.save(commit=False)
                notification.user = request.user
                notification.save()
                return HttpResponseRedirect('/')
        else:
            form = NotificationForm()

        workshifts = request.user.workshift_set.all()
        today_past_shifts = []
        today_future_shifts = []
        for shift in workshifts:
            in_time = shift.scheduled_in
            out_time = shift.scheduled_out
            if (in_time.year == now.year and in_time.month == now.month and in_time.day == now.day):
                if now - out_time > datetime.timedelta(seconds=1):
                    today_past_shifts.append(shift)
                else:
                    today_future_shifts.append(shift)
        args = {
            'request': request,
            'locations': locations,
            'clockin_time': clockin_time,
            'today_past_shifts': today_past_shifts,
            'today_future_shifts': today_future_shifts,
            'events': events,
            'alerts': alerts,
            'can_Add': can_Add,
        }
        return render_to_response('dashboard.html', locals(), context_instance=RequestContext(request))
    else:
        return render_to_response('hello.html', locals())


def labgeeks_login(request):
    """ Login a user. Called by the @login_required decorator.
    """

    # Get a token to protect from cross-site request forgery
    c = {}
    c.update(csrf(request))
    if request.user.is_authenticated():
        try:
            return HttpResponseRedirect(request.GET['next'])
        except:
            return HttpResponseRedirect('/')
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    try:
                        return HttpResponseRedirect(request.GET['next'])
                    except:
                        #Redirects to the dashboard.
                        return HttpResponseRedirect('/')
                else:
                    # Return a disabled account error
                    return HttpResponseRedirect('/inactive/')
    else:
        form = LoginForm()

    return render_to_response('login.html', locals(), context_instance=RequestContext(request))


def labgeeks_logout(request):
    """ Manually log a user out.
    """
    logout(request)
    return HttpResponseRedirect('/')


def inactive(request):
    """ Return if a user's account has been disabled.
    """
    return render_to_response('inactive.html', locals())
