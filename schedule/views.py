from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from people.models import UserProfile
from chronos.models import Location
from schedule.models import *
from schedule.forms import SelectTimePeriodForm, SelectDailyScheduleForm, CreateDailyScheduleForm
from django import forms
import json
from datetime import date, datetime, timedelta


def list_options(request):
    '''
    Lists out the options regarding scheduling. Essentially a home page for the schedule app.
    '''

    if not request.user.is_authenticated():
        message = 'Permission Denied'
        reason = 'You do not have permission to visit this part of the page.'
        return render_to_response('fail.html', locals(), context_instance=RequestContext(request))

    return render_to_response('schedule_home.html', locals(), context_instance=RequestContext(request))


def view_available_shifts(request):
    ''' Display a list of all available shifts. (Shifts that have no user attached to them)
    '''
    #Grab all available shifts
    data = WorkShift.objects.filter(person=None)

    shifts = []
    for shift in data:
        x = {'day': shift.scheduled_in.date(), 'scheduled_in': shift.scheduled_in.time(), 'scheduled_out': shift.scheduled_out.time(), 'location': shift.location}
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
            data = WorkShift.objects.filter(
                scheduled_in__day=day.day,
                scheduled_in__month=day.month,
                scheduled_in__year=day.year,
                person__isnull=False,
                location__name=location
            ).order_by('person__username')

            if not data:
                message = 'Nobody scheduled for %s' % (day)
            else:

                # TODO EDIT LATER
                x_axis = []
                y_axis = []

                # y_axis - The time scale
                counter = datetime(day.year, day.month, day.day, 7, 0)

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
                    x = {'time': time.strftime('%I:%M %p').lower(), 'people': [], 'class': "row"}

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

    return render_to_response('view_shifts.html', locals(), context_instance=RequestContext(request))


def view_timeperiods(request):
    '''
    This view returns a list of timeperiods and users who can work in those timeperiods.
    This view also allows users to select which timeperiods they can work for.
    '''
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect("/people/%s" % user.username)

    timeperiod_stats = []
    timeperiods = TimePeriod.objects.all().order_by('start_date')
    if request.method == 'POST':
        form = SelectTimePeriodForm(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile = form.save()
    else:
        form = SelectTimePeriodForm(instance=user_profile)

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

    return render_to_response('view_timeperiods.html', locals(), context_instance=RequestContext(request))


def view_timeperiod_data(request):
    '''
    This method returns json data regarding timeperiods.
    '''
    data = request.REQUEST.copy()
    slug = data.getlist('name')[0]

    timeperiod = TimePeriod.objects.get(slug=slug)
    people_list = UserProfile.objects.filter(working_periods__name=timeperiod.name)
    people = [str(c.user) for c in people_list]
    result = json.dumps({
        'timeperiod': timeperiod.name,
        'start_date': timeperiod.start_date.strftime('%b. %d, %Y'),
        'end_date': timeperiod.end_date.strftime('%b. %d, %Y'),
        'count': len(people),
        'people': people
    })

    return HttpResponse(result)


def view_people(request):
    '''
    This method returns a list of all users in the system in json.
    '''
    people_list = User.objects.all()
    people = [str(c.username) for c in people_list]
    result = json.dumps({'people': people})

    return HttpResponse(result)


def create_default_schedule(request):
    '''
    This view will allow users to create a schedule from scratch.
    '''

    if request.method == 'POST':
        form = CreateDailyScheduleForm(request.POST)
        if form.is_valid():

            # Grab the data from the form
            timeperiod = TimePeriod.objects.get(name=form.cleaned_data['timeperiods'])
            location = Location.objects.get(name=form.cleaned_data['location'])

            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

            # Create a schedule dictionary to hold the data.
            base_schedule = []
            schedule = []

            # Grab the closed hours and default shifts used in a timeperiod.
            closing_hours = ClosedHour.objects.filter(location=location, timeperiod=timeperiod)
            default_shifts = DefaultShift.objects.filter(location=location, timeperiod=timeperiod)
            base_shifts = BaseShift.objects.filter(location=location, timeperiod=timeperiod)
            time_in = time(7, 45)
            time_out = time(11, 45)

            Shift_Types = []
            closing_ranges = {
                'Monday': [],
                'Tuesday': [],
                'Wednesday': [],
                'Thursday': [],
                'Friday': [],
                'Saturday': [],
                'Sunday': [],
            }

            shift_ranges = {
                'Monday': [],
                'Tuesday': [],
                'Wednesday': [],
                'Thursday': [],
                'Friday': [],
                'Saturday': [],
                'Sunday': [],
            }

            base_shift_ranges = {
                'Monday': [],
                'Tuesday': [],
                'Wednesday': [],
                'Thursday': [],
                'Friday': [],
                'Saturday': [],
                'Sunday': [],
            }
            base_shift_hours = {
                'Monday': [],
                'Tuesday': [],
                'Wednesday': [],
                'Thursday': [],
                'Friday': [],
                'Saturday': [],
                'Sunday': [],
            }
            # TODO: Form a less redundant way of doing the hour ranges.
            # Find out which hours were closing hours
            ''' going to use base shifts to determine closing hours when changing the schedule now
            for closing_hour in closing_hours:
                day = closing_hour.day
                in_time = closing_hour.in_time
                out_time = closing_hour.out_time
                hours = []

                current = datetime(1,1,1,in_time.hour,in_time.minute)

                while current.time() != out_time:
                    hours.append(current.time())
                    current += timedelta(minutes=30)
                hours.append(current.time())

                closing_ranges[day] += hours
            '''
            for shift in base_shifts:
                day = shift.day
                in_time = shift.in_time
                out_time = shift.out_time
                hours = []

                current = datetime(1, 1, 1, in_time.hour, in_time.minute)

                while current.time() != out_time:
                    hours.append(current.time())
                    current += timedelta(minutes=30)
                base_shift_hours[day] += hours
                if shift.shift_type:
                    groups = ''
                    count = 0
                    users = []
                    for group in shift.shift_type.allowed_groups.get_query_set():
                        if count == 0:
                            groups += group.name
                        else:
                            groups += ', ' + group.name
                        count = 1
                        count1 = 0
                        for user in group.user_set.values():
                                users.append(user['username'])
                    if not {'name': shift.shift_type.name, 'users': users} in Shift_Types:
                        Shift_Types.append({'name': shift.shift_type.name, 'users': users})
                    base_shift_ranges[day].append({'hours': hours, 'name': shift.shift_type.name})
                else:
                    base_shift_ranges[day].append({'hours': hours, 'name': 'Open_Shift'})

            for day in base_shift_hours:
                if len(base_shift_hours[day]) > 0:
                    in_time = time(7, 45)
                    out_time = time(23, 45)
                    hours = []
                    while base_shift_hours[day].count(in_time) == 0:
                        hours.append(in_time)
                        if in_time.minute == 45:
                            in_time = in_time.replace(hour=in_time.hour + 1, minute=15)
                        elif in_time.minute == 15:
                            in_time = in_time.replace(minute=45)
                    while base_shift_hours[day].count(out_time) == 0:
                        if hours.count(out_time) == 0:
                            hours.append(out_time)
                        if out_time.minute == 45:
                            out_time = out_time.replace(minute=15)
                        elif out_time.minute == 15:
                            out_time = out_time.replace(hour=out_time.hour - 1, minute=45)
                    closing_ranges[day] += hours
            # Find out which hours were shift hours.
            for shift in default_shifts:
                #currently does nothing if there is no person set to the shift
                if shift.person:
                    day = shift.day
                    in_time = shift.in_time
                    out_time = shift.out_time
                    hours = []

                    current = datetime(1, 1, 1, in_time.hour, in_time.minute)

                    while current.time() != out_time:
                        hours.append(current.time())
                        current += timedelta(minutes=30)

                    shift_ranges[day].append({'hours': hours, 'user': shift.person.username})
            # TODO: For now, create an arbitrary size for the schedule. Consider changing it in the future.
            schedule_length = [0] * 10

            # Now append append the hours to each day in the schedule.
            for day in days:
                closing_range = closing_ranges[day]
                shift_range = shift_ranges[day]
                base_shift_range = base_shift_ranges[day]
                times = []
                base_times = []
                counter = datetime(1, 1, 1, 7, 45)

                # Loop through the time and start appending the rows to each time.
                while counter.hour != 0:
                    row = []
                    base_row = []
                    if counter.time() in closing_range:
                        # Fill in the closing hours
                        for i in range(len(schedule_length)):
                            row.append({'class': 'closed_hours', 'user': 'closed'})
                            base_row.append({'class': 'closed_hours', 'user': 'closed'})
                    else:
                        # Fill in the shift hours.
                        count = 0
                        for shift in base_shift_range:

                            if counter.time() in shift['hours']:
                                count += 1
                                base_row.append({'class': None, 'name': shift['name']})

                        for i in range(len(schedule_length) - count):
                            base_row.append({'class': None, 'user': None})
                        count = 0
                        for shift in shift_range:

                            if counter.time() in shift['hours']:
                                count += 1
                                row.append({'class': None, 'user': shift['user']})

                        for i in range(len(schedule_length) - count):
                            row.append({'class': None, 'user': None})

                    # Append the row and time
                    times.append({'time': counter.time().strftime('%I:%M %p').lower(), 'row': row})
                    base_times.append({'time': counter.time().strftime('%I:%M %p').lower(), 'row': base_row})

                    # Increment by 30 minutes
                    counter += timedelta(minutes=30)

                # Append the time row to the schedule.
                schedule.append({'times': times, 'day': day})
                base_schedule.append({'times': base_times, 'day': day})

            schedule_class = "visible"

            # Determine if the user can edit the schedule.
            if request.user.has_perm('schedule.add_defaultshift'):
                can_edit_schedule = True
            else:
                can_edit_scehdule = False
    else:
        # There is no schedule to display.
        schedule_class = "hidden"
        form = CreateDailyScheduleForm()

    return render_to_response('create_schedule.html', locals(), context_instance=RequestContext(request))


def save_hours(request):
    '''
    This method is used to process an ajax request and save the closed hours in the schedule app.
    '''
    data = request.POST.copy()
    hours = {
        'Monday': data.getlist('Monday'),
        'Tuesday': data.getlist('Tuesday'),
        'Wednesday': data.getlist('Wednesday'),
        'Thursday': data.getlist('Thursday'),
        'Friday': data.getlist('Friday'),
        'Saturday': data.getlist('Saturday'),
        'Sunday': data.getlist('Sunday'),
    }
    username = data.getlist('user')
    loc = data.getlist('location')[0]
    tp = data.getlist('timeperiod')[0]
    location = Location.objects.get(name=loc)
    timeperiod = TimePeriod.objects.get(name=tp)
    tmpdsdate = timeperiod.start_date
    mondays = []
    tuesdays = []
    wednesdays = []
    thursdays = []
    fridays = []
    saturdays = []
    sundays = []
    days = [mondays, tuesdays, wednesdays, thursdays, fridays, saturdays, sundays]
    try:
        tmpdedate1 = timeperiod.end_date.replace(day=timeperiod.end_date.day + 1)
    except:
        if timeperiod.end_date.month == 12:
            tmpdedate1 = date(timeperiod.end_date.year + 1, 1, 1)
        else:
            tmpdedate1 = timeperiod.end_date.replace(month=timeperiod.end_date.month + 1, day=1)
    while tmpdsdate != tmpdedate1:
        days[tmpdsdate.weekday()].append(tmpdsdate)
        try:
            tmpdsdate = tmpdsdate.replace(day=tmpdsdate.day + 1)
        except:
            if tmpdsdate.month == 12:
                tmpdsdate = date(tmpdsdate.year + 1, 1, 1)
            else:
                tmpdsdate = tmpdsdate.replace(month=tmpdsdate.month + 1, day=1)
    # Save the results in to a dictionary.
    if username:
        user = User.objects.get(username=username[0])
        WorkShift.objects.filter(person=user, location=location).delete()
    else:
        user = None
    result = {}

    # Loop through the hours that are going to be saved.
    for day, hours_list in hours.iteritems():
        # TODO: Figure out how to delete correct shifts. As of now, this will be only delete a user's shift who appears on the schedule.
        if user:
            DefaultShift.objects.filter(location=location, timeperiod=timeperiod, day=day, person=user).delete()
        else:
            ClosedHour.objects.filter(location=location, timeperiod=timeperiod, day=day).delete()
        if len(hours_list) > 0:
            time_ranges = return_time_ranges(hours_list)
            for time_range in time_ranges:
                in_time = time_range['in_time'].time()
                out_time = time_range['out_time'].time()
                # Save the hours, depending on which type of hours they are.
                if user:
                    week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    ind = week.index(day)
                    shift_days = days[week.index(day)]
                    for day1 in shift_days:
                        in_time1 = in_time
                        while in_time1 != out_time:
                            time_in = datetime(day1.year, day1.month, day1.day, in_time1.hour, in_time1.minute)
                            if in_time1.minute == 45:
                                in_time1 = in_time1.replace(hour=in_time1.hour + 1, minute=15)
                            elif in_time1.minute == 15:
                                in_time1 = in_time1.replace(minute=45)
                            time_out = datetime(day1.year, day1.month, day1.day, in_time1.hour, in_time1.minute)
                            employee_work_hour = WorkShift.objects.create(
                                person=user,
                                scheduled_in=time_in,
                                scheduled_out=time_out,
                                location=location,
                            )
                    employee_hour = DefaultShift.objects.create(
                        person=user,
                        day=day,
                        in_time=in_time,
                        out_time=out_time,
                        location=location,
                        timeperiod=timeperiod,
                    )
                    name = user.username
                else:
                    closed_hour = ClosedHour.objects.create(
                        day=day,
                        in_time=in_time,
                        out_time=out_time,
                        location=location,
                        timeperiod=timeperiod,
                    )
                    name = None

                # Append the data in a string format for Json.
                string_time = {'user': name, 'in_time': time_range['in_time_string'], 'out_time': time_range['out_time_string']}

                try:
                    result[day].append(string_time)
                except:
                    result[day] = [string_time]

    # Return the results and let the ajax call handle this data.
    result = json.dumps(result)
    return HttpResponse(result)


def return_time_ranges(hours_list):
    '''
    This method will return a hour ranges from a list of hours.
    e.g. hours_list = [9:00,9:30,10:00,1:00,1:30,2:00] will return [{'in_time': 9:00, 'out_time':10:00} {'in_time': 1:00, 'out_time': 2:00}]
    '''

    # TIME FORMATTING:
    time_format = '%I:%M %p'
    time_ranges = []

    in_time = None
    out_time = None
    hours_list1 = []
    for hour in hours_list:
        hour = datetime.strptime(hour, time_format)
        hours_list1.append(hour)
    hours_list1.sort()
    for hour in hours_list1:
        #current = datetime.strptime(hour,time_format)
        current = hour
        if not in_time and not out_time:
            in_time = current
            out_time = current
            if out_time.minute == 45:
                out_time = out_time.replace(hour=out_time.hour + 1, minute=15)
            elif out_time.minute == 15:
                out_time = out_time.replace(minute=45)
        elif (current == out_time):
            if out_time.minute == 45:
                out_time = out_time.replace(hour=out_time.hour + 1, minute=15)
            elif out_time.minute == 15:
                out_time = out_time.replace(minute=45)
        else:
            time_range = {'in_time': in_time, 'out_time': out_time, 'in_time_string': in_time.strftime('%I:%M %p').lower(), 'out_time_string': out_time.strftime('%I:%M %p').lower()}
            time_ranges.append(time_range)
            in_time = current
            out_time = current
            if out_time.minute == 45:
                out_time = out_time.replace(hour=out_time.hour + 1, minute=15)
            elif out_time.minute == 15:
                out_time = out_time.replace(minute=45)
    time_range = {'in_time': in_time, 'out_time': out_time, 'in_time_string': in_time.strftime('%I:%M %p').lower(), 'out_time_string': out_time.strftime('%I:%M %p').lower()}
    time_ranges.append(time_range)

    return time_ranges


def view_preferences(request, form):
    pass
