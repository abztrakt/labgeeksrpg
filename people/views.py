from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from calendar import HTMLCalendar
from datetime import date
from django.utils.safestring import mark_safe

import chronos.models as models 

@login_required
def list_all(request):
    """ List all users in the system.
    """
    users = User.objects.filter(is_active=True)
    return render_to_response('list.html', locals(), context_instance=RequestContext(request))

@login_required
def view_profile(request, name):
    """ Show a user profile.
    """
    #profile = request.user.get_profile()
    return render_to_response('profile.html', locals())

@login_required
def view_specific_timesheet(request,name,year,month):
    return view_timesheet(request,name,date(int(year),int(month),1))

@login_required
def view_timesheet(request,name, target_date=date.today()):
    """ Show the timesheet of the user
    """
    args = {}

    month = target_date.month
    year = target_date.year

    #Grab the user and their shifts.
    user = User.objects.filter(username = name)
    shifts = models.Shift.objects.filter(person = user, intime__month = month, intime__year = year)

    args['user'] = user[0]
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

    cal = TimesheetCalendar(shifts).formatmonth(year,month)
    args['calendar'] = mark_safe(cal)
    return render_to_response('timesheet.html',args)

class TimesheetCalendar(HTMLCalendar):
    """ This class is used for displaying the timesheet in a calendar format
    """
    
    def __init__(self,shifts):
        super(TimesheetCalendar,self).__init__()
        self.shifts = self.group_by_day(shifts)
    
    def formatday(self,day,weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if day <= 15:
                cssclass += ' first'
            else:
                cssclass += ' second'
            s = '<strong>%s</strong>' % (day)
            if date.today() == date(self.year,self.month,day):
                cssclass += ' today'
            if day in self.shifts:
                cssclass += ' filled'
                total_hours = 0
                for shift in self.shifts[day]:
                    if shift.outtime:
                        total_hours += float(shift.length())
                body = '<p>Total Hours: <strong class="hours">' + str(total_hours) + '</strong></p>'
                s += '%s' % (body)
                return self.day_cell(cssclass, s)
            return self.day_cell(cssclass, s)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(TimesheetCalendar,self).formatmonth(year,month)

    def group_by_day(self, shifts):
        shifts_by_day = {}
        for shift in shifts:
            if shift.intime.day in shifts_by_day:
                shifts_by_day[shift.intime.day].append(shift)
            else:
                shifts_by_day[shift.intime.day] = [shift]
        return shifts_by_day
    
    def day_cell(self,cssclass,body):
        return '<td class="%s">%s</td>' % (cssclass,body)
