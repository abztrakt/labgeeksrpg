from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse
from people.models import UserProfile, TimePeriod
from chronos.models import Location
from schedule.models import *
from schedule.forms import SelectTimePeriodForm, SelectDailyScheduleForm, CreateDailyScheduleForm
from django import forms
import json
#EDIT LATER
from datetime import date, datetime, time, timedelta
def list_options(request):

    if not request.user.is_superuser:
        message = 'Permission Denied'
        reason = 'You do not have permission to visit this part of the page.'
        return render_to_response('fail.html', locals(),context_instance=RequestContext(request))

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
            location = form.cleaned_data['location']
            data = WorkShift.objects.filter(scheduled_in__day=day.day,scheduled_in__month=day.month,scheduled_in__year=day.year,person__isnull=False,location__name=location).order_by('person__username')
            if not data:
                message = 'Nobody scheduled for %s' %  (day)
            else:

                # TODO EDIT LATER
                x_axis = []
                y_axis = []

                # x_axis
                # maybe dont need this... for now.
                '''
                weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                starting = day - timedelta(days = day.weekday())
                for i in range(0,7):
                    x = {'day' : weekdays[i],'date':starting + timedelta(days = i)}
                    x_axis.append(x)
                '''

                # y_axis - The time scale
                counter = datetime(day.year,day.month,day.day,7,0)
                
                while counter.hour != 1:
                    y_axis.append(counter.time())
                    counter += timedelta(minutes=30)
                
                #Grab the unique users from the shifts.
                unique_people = data.values('person__username').distinct()
                people = []
                for person in unique_people:
                    people.append(person['person__username'])

                # Content - fill in the grid with the user's name to show that they are working that time frame.
                shifts = []
                now = datetime.time(datetime.now())

                for time in y_axis:
                    x = {'time':time.strftime('%I:%M %p').lower(),'people':[],'class':"row"}
                    
                    if time.hour == now.hour:
                        x['class'] += " now"

                    group = {}
                    for shift in data:
                        if shift.scheduled_in.time() <= time and shift.scheduled_out.time() >= time:
                            group[shift.person.username] = shift.person
                        elif shift.person.username not in group.keys():
                            group[shift.person.username] = None

                    for person in people:
                        if not group[person]:
                            x['people'].append(None)
                        else:
                            x['people'].append(person)
                    shifts.append(x)

                # The total columns in the schedule.
                rowlength = len(people) + 1
        
    else:
        form = SelectDailyScheduleForm()

    return render_to_response('view_shifts.html', locals(),context_instance=RequestContext(request))

def view_timeperiods(request):
    timeperiod_stats = []
    timeperiods = TimePeriod.objects.all().order_by('start_date')

    for timeperiod in timeperiods:
        people = UserProfile.objects.filter(working_periods__name=timeperiod.name)
        data = {
            'timeperiod': timeperiod.name,
            'count': people.count(),
            'slug': timeperiod.slug
            }

        timeperiod_stats.append(data)
    if not timeperiods:
        message = 'Nobody available for timeperiods or nobody filled out preferences'
     
    return render_to_response('view_timeperiods.html',locals(),context_instance=RequestContext(request))

def view_timeperiod_data(request):
    data = request.REQUEST.copy()
    slug = data.getlist('name')[0]
    
    
    timeperiod = TimePeriod.objects.get(slug=slug)
    people_list = UserProfile.objects.filter(working_periods__name=timeperiod.name)
    people = [str(c.user) for c in people_list]
    result = json.dumps({
        'timeperiod':timeperiod.name,
        'start_date': timeperiod.start_date.strftime('%b. %d, %Y'),
        'end_date': timeperiod.end_date.strftime('%b. %d, %Y'),
        'count': len(people),
        'people': people
        })

    return HttpResponse(result)

def view_people(request):
    #TODO change it so that only active people are displayed.
    people_list = User.objects.all()
    people = [str(c.username) for c in people_list]
    result = json.dumps({
        'people': people
        })

    return HttpResponse(result)


def create_default_schedule(request):
    if request.method == 'POST':
        form = CreateDailyScheduleForm(request.POST)
        if form.is_valid():

            # Grab the data from the form
            timeperiod = TimePeriod.objects.get(name=form.cleaned_data['timeperiods'])
            location = Location.objects.get(name=form.cleaned_data['location'])

            # TODO add timeperiod with a default shift instead of looking up start date / end date.
            start_date = timeperiod.start_date
            end_date = timeperiod.end_date
            
            x_axis = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            y_axis = []

            # y_axis - The time scale
            counter = datetime(1,1,1,7,0)
            
            while counter.hour != 1:
                y_axis.append(counter.time().strftime('%I:%M %p').lower())
                counter += timedelta(minutes=30)
            
            shifts = []
            for day in x_axis:
                data = {'day': day,'shifts':y_axis,'location':location}
                shifts.append(data)

            schedule_class = "visible"
            #import pdb; pdb.set_trace()
    else:
        schedule_class ="hidden"
        form = CreateDailyScheduleForm()
    
    return render_to_response('create_schedule.html', locals(), context_instance=RequestContext(request))

def view_preferences(request,form):
    pass
