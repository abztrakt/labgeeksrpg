from calendar import HTMLCalendar
from datetime import date


class TimesheetCalendar(HTMLCalendar):
    """ This class is used for displaying the timesheet in a calendar format
    """

    def __init__(self, shifts, user=None):
        super(TimesheetCalendar, self).__init__()
        self.shifts = self.group_by_day(shifts)
        self.personal = self.is_personal(shifts)
        if user:
            self.user = user
            #self.can_view_shifts = self.is_staff(request,user)
        else:
            self.user = ''

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if day <= 15:
                cssclass += ' first'
            else:
                cssclass += ' second'
            s = '<strong>%s</strong>' % (day)
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.shifts:
                cssclass += ' filled'
                total_hours = 0
                for shift in self.shifts[day]:
                    if shift.outtime:
                        total_hours += float(shift.length())
                body = '<p><a href="/chronos/%s/%s/%s/%s"><i class="icon-list-alt"></i><span class="long">Total Hours: <strong class="hours">' % (self.user.username, self.year, self.month, day) + str(total_hours) + '</strong></span></a></p>'
                s += '%s' % (body)
                return self.day_cell(cssclass, s)
            return self.day_cell(cssclass, s)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(TimesheetCalendar, self).formatmonth(year, month)

    def group_by_day(self, shifts):
        shifts_by_day = {}
        for shift in shifts:
            if shift.intime.day in shifts_by_day:
                shifts_by_day[shift.intime.day].append(shift)
            else:
                shifts_by_day[shift.intime.day] = [shift]
        return shifts_by_day

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

    def is_personal(self, shifts):
        if shifts:
            user = shifts[0].person
            for shift in shifts:
                if shift.person != user:
                    #Calendar is not personal, used for multiple all staff
                    return False
        return True

    def is_staff(self, request, user):
        if request.user.is_staff or request.user == user:
            return True
        return False


class ReportCalendar(TimesheetCalendar):
    """ This class is used for displaying the reports in a monthly calendar
    format.
        Overrides the TimesheetCalendar class by injecting the ability to view
    shifts of a the given day.
    """

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if day <= 15:
                cssclass += ' first'
            else:
                cssclass += ' second'
            s = '<strong>%s</strong>' % (day)
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.shifts:
                s += '<p><a href="/chronos/report/%s/%s/%s"><i class="icon-list-alt"></i><span class="long">Shift Details</span></a></p>' % (self.year, self.month, day)

                return super(ReportCalendar, self).day_cell(cssclass, s)
            return super(ReportCalendar, self).day_cell(cssclass, s)
        return super(ReportCalendar, self).day_cell('noday', '&nbsp;')
