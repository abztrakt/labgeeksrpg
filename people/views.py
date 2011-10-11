from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from datetime import date
from django.utils.safestring import mark_safe

import chronos.models as models 
from labgeeksrpg.utils import TimesheetCalendar
from people.forms import *
from people.models import UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile

@login_required
def list_all(request):
    """ List all users in the system. (Alphabetically, ignoring case)
    """
    users = User.objects.filter(is_active=True).extra(select={'username_upper': 'upper(username)'}, order_by=['username_upper'])
    return render_to_response('list.html', locals(), context_instance=RequestContext(request))

@login_required
def view_profile(request, name):
    """ Show a user profile.
    """

    this_user = User.objects.get(username=name)
    if UserProfile.objects.filter(user=this_user): 
        #User has already created a user profile.
        profile = UserProfile.objects.get(user=this_user)

        if request.user.__str__() == name or request.user.is_superuser:
            edit = True

        return render_to_response('profile.html', locals())
    else:
        #User HAS NOT created a user profile, allow them to create one.
        return create_user_profile(request,name)

@login_required
def create_user_profile(request,name):
    """ This view is called when creating or editing a user profile to the system.
        Allows the user to edit and display certain things about their information.
    """
    c = {}
    c.update(csrf(request))

    if request.user.__str__() != name and not request.user.is_superuser:
        # Don't allow editing of other people's profiles.
        return render_to_response('not_your_profile.html',locals(),context_instance=RequestContext(request))

    #Grab the user that the name belongs to and check to see if they have an existing profile.
    user = User.objects.get(username=name)
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = CreateUserProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            if profile:
                # Update the user profile
                profile = form.save()
            else:
                # Create a user profile, but DON'T add to database quite yet.
                profile = form.save(commit=False)

                # Add user to the profile and save
                profile.user = user
                profile.save()

                # Now, save the many-to-many data for the form (Required when commit=False)
                form.save_m2m()

            # Allow editing right after creating/editing a profile.
            edit = True
            # View the profile
            return render_to_response('profile.html',locals(),context_instance=RequestContext(request))
    else:
        form = CreateUserProfileForm(instance=profile)

    # Differentiate between a super user creating a profile or a person creating their own profile.
    this_user = request.user
    if profile:
        message = "You are editing a user profile for "
    else:
        message = "You are creating a user profile for "

    if this_user.__str__() == name:
        message += "yourself."
    else:
        message += name + "."

    return render_to_response('create_profile.html',locals(),context_instance=RequestContext(request))

@login_required
def view_shifts_timesheet(request,name,year,month,day):

    if not request.user.is_staff:
        message = 'Permission Denied'
        reason = 'You do not have permission to visit this part of the page.'
        return render_to_response('fail.html',locals(),context_instance=RequestContext(request))
    user = User.objects.get(username=name)
    shifts = models.Shift.objects.filter(person = user, intime__month = month, intime__year = year, intime__day = day)
    return render_to_response('specific_report.html', locals(), context_instance=RequestContext(request))

@login_required
def view_specific_timesheet(request,name,year,month):
    return view_timesheet(request,name,date(int(year),int(month),1))

@login_required
def view_timesheet(request,name, target_date=None):
    """ Show the timesheet of the user
    """
    args = {}
    if not target_date:
        target_date = date.today()

    month = target_date.month
    year = target_date.year

    #Grab the user and their shifts.
    user = User.objects.get(username = name)
    shifts = models.Shift.objects.filter(person = user, intime__month = month, intime__year = year)

    args['user'] = user
    args['date'] = target_date
    
    #Figure out the prev and next months
    if target_date.month == 1:
        #Its January
        args['prev_date'] = date(year-1,12,1)
        args['next_date'] = date(year, 2,1)
    elif target_date.month == 12:
        #Its December
        args['prev_date'] = date(year, 11,1)
        args['next_date'] = date(year+1,1,1)
    else:
        #Its a regular month
        args['prev_date'] = date(year,month-1,1)
        args['next_date'] = date(year,month+1,1)

    # Figure out total hours were worked in pay periods and in weeks
    args['payperiod_totals'] = {'first':0,'second':0}
    weekly = {}
    first_week = date(year,month,1).isocalendar()[1]
    for shift in shifts:
        if shift.outtime:
            shift_date = shift.intime
            length = float(shift.length())

            #Keep track of pay period totals
            if shift_date.day <= 15:
                #1st pay period
                args['payperiod_totals']['first'] += length
            else:
                #2nd pay period
                args['payperiod_totals']['second'] += length

            #Keep track of weekly totals
            week_number = shift_date.isocalendar()[1] - first_week + 1
            if week_number in weekly:
                weekly[week_number] += length
            else:
                weekly[week_number] = length
    
    #Sort the weekly totals
    weekly = sorted(weekly.items())
    args['weekly_totals'] = []
    for i in range(0,len(weekly)):
        args['weekly_totals'].append({'week':weekly[i][0],'total':weekly[i][1]})

    cal = TimesheetCalendar(shifts,request,user).formatmonth(year,month)
    args['calendar'] = mark_safe(cal)
    args['request'] = request
    return render_to_response('timesheet.html',args)
