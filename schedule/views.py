from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf

from people.models import UserProfile, TimePeriod
from schedule.models import *
from schedule.forms import *

def list_options(request):
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

    if not timeperiods:
        message = 'Nobody available for timeperiods or nobody filled out preferences'
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

def view_available_shifts(request):
    ''' Display a list of all available shifts. (Shifts that have no user attached to them)
    '''
    #Grab all available shifts
    data = WorkShift.objects.filter(person=None)

    shifts=[]
    for shift in data:
        x = {'day':shift.scheduled_in.date(),'scheduled_in':shift.scheduled_in.time(),'scheduled_out':shift.scheduled_out.time(),'location':shift.location}
        shifts.append(x)
    
    if not shifts:
        message = "No available shifts."

    return render_to_response('available.html', locals(), context_instance=RequestContext(request))

def view_shifts(request):
    ''' Display a list of scheduled work shifts. Allows user to specify which day they want to look at.
    '''
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        form = SelectDailyScheduleForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            data = WorkShift.objects.filter(scheduled_in__day=day.day,scheduled_in__month=day.month,scheduled_in__year=day.year,person__isnull=False)
            shifts = []
            for shift in data:
                x = {'person':shift.person,'day':shift.scheduled_in.date(),'scheduled_in':shift.scheduled_in.time(),'scheduled_out':shift.scheduled_out.time(),'location':shift.location}
                shifts.append(x)

            if not data:
                message = 'Nobody scheduled for %s' %  (day)
        
    else:
        form = SelectDailyScheduleForm()

    return render_to_response('view_shifts.html', locals(),context_instance=RequestContext(request))

def view_preferences(request,form):

    message = "YOU GOT HERE."
    return render_to_response('schedule_home.html',locals(),context_instance=RequestContext(request))


def edit_preferences(request):
    return render_to_response('schedule_home.html',locals(), context_instance=RequestContext(request))
