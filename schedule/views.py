from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf

from people.models import UserProfile, TimePeriod
from schedule.models import *
from schedule.forms import *

def list_options(request):

    if not request.user.is_superuser:
        message = 'Permission Denied'
        reason = 'You do not have permission to visit this part of the page.'
        return render_to_response('fail.html', locals(),context_instance=RequestContext(request))

    c = {}
    c.update(csrf(request))

    timeperiod_stats = []
    timeperiod_users = []
    timeperiods = TimePeriod.objects.all().order_by('start_date')

    for timeperiod in timeperiods:
        people = UserProfile.objects.filter(working_periods__name=timeperiod.name)
        data = {
            'timeperiod': timeperiod.name,
            'start_date': timeperiod.start_date,
            'end_date': timeperiod.end_date,
            'count': people.count()
            }

        users = {
            'timeperiod': timeperiod.name,
            'people': people
        }
        timeperiod_stats.append(data)
        timeperiod_users.append(users)
    
    if request.method == 'POST':
        form = SelectDailyScheduleForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            data = WorkShift.objects.filter(scheduled_in__day=day.day,scheduled_in__month=day.month,scheduled_in__year=day.year)
            shifts = []
            for shift in data:
                x = {'person':shift.person,'day':shift.scheduled_in.date(),'scheduled_in':shift.scheduled_in.time(),'scheduled_out':shift.scheduled_out.time(),'location':shift.location}
                shifts.append(x)
    else:
        form = SelectDailyScheduleForm()

    """
    if request.method == 'POST':
        form = SelectTimePeriodForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            filter_choice = data['time_period_filter']
            if 'avail' in filter_choice:
                return view_availability(request,form)
            elif 'prefs' in filter_choice:
                return view_preferences(request,form)
    else:
        form = SelectTimePeriodForm()

    message = "No timeperiod selected."
    """
    return render_to_response('schedule_home.html',locals(), context_instance=RequestContext(request))

def view_availability(request,form):
    timeperiod = form.cleaned_data['time_periods']

    #Display all of the users who have selected this timeperiod as an available timeperiod.
    people = UserProfile.objects.filter(working_periods__name=timeperiod)

    if people:
        message = "Below is the list of people who can work this time period."
    else:
        message = "Nobody available, or nobody filled out preferences in their profile."

    total = people.count()
    return render_to_response('schedule_home.html', locals(), context_instance=RequestContext(request))


def view_preferences(request,form):

    message = "YOU GOT HERE."
    return render_to_response('schedule_home.html',locals(),context_instance=RequestContext(request))


def edit_preferences(request):
    return render_to_response('schedule_home.html',locals(), context_instance=RequestContext(request))
