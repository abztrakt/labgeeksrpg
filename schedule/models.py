from django.db import models
from django.contrib.auth.models import User, Group
from labgeeksrpg.chronos.models import Location
from datetime import date, time


class TimePeriod(models.Model):
    """ Defines possible periods of time when a person could choose to work or choose not to work.
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    start_date = models.DateField(default=date.today())
    end_date = models.DateField(default=date.today())

    def __unicode__(self):
        return self.name


class WorkShift(models.Model):
    """ These are shifts that people are expected to work for.
    """
    person = models.ForeignKey(User, null=True, blank=True)
    scheduled_in = models.DateTimeField()
    scheduled_out = models.DateTimeField()
    location = models.ForeignKey(Location)

    def __unicode__(self):
        if self.person:
            person_string = self.person
        else:
            person_string = "Open Shift"

        return "%s: [%s] %s-%s @%s" % (person_string, self.scheduled_in.date(), self.scheduled_in.time(), self.scheduled_out.time(), self.location)


class ShiftType(models.Model):
    '''defines a type of schedule for a location and timeperiod, and time of day.
    Also defines what groups of people are allowed to work in this time
    '''
    allowed_groups = models.ManyToManyField(Group)
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return "%s" % (self.name)


class DefaultShift(models.Model):
    DAY_CHOICES = (
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )
    person = models.ForeignKey(User, null=True, blank=True)
    day = models.CharField(max_length=256, choices=DAY_CHOICES)
    in_time = models.TimeField()
    out_time = models.TimeField()
    location = models.ForeignKey(Location)
    timeperiod = models.ForeignKey(TimePeriod, null=True, blank=True)

    def __unicode__(self):
        if self.person:
            person_string = self.person
        else:
            person_string = "Open Shift"

        return "%s: [%s] %s-%s @%s" % (person_string, self.day, self.in_time, self.out_time, self.location)


class BaseShift(models.Model):
    '''this is a base shift designed to outline the hours and rules that a schedule should follow.
    default and work shifts should only be created for a location/timeperiod during times a base shift has set
    '''
    DAY_CHOICES = (
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )
    day = models.CharField(max_length=256, choices=DAY_CHOICES)
    in_time = models.TimeField()
    out_time = models.TimeField()
    location = models.ForeignKey(Location)
    timeperiod = models.ForeignKey(TimePeriod, null=True, blank=True)
    shift_type = models.ForeignKey(ShiftType, null=True, blank=True)

    def __unicode__(self):
        if self.shift_type:
            shift_string = self.shift_type.name
        else:
            shift_string = 'Open Shift'
        return "%s: [%s] %s-%s @%s" % (shift_string, self.day, self.in_time, self.out_time, self.location)


class ClosedHour(models.Model):
    DAY_CHOICES = (
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )
    day = models.CharField(max_length=256, choices=DAY_CHOICES)
    in_time = models.TimeField()
    out_time = models.TimeField()
    location = models.ForeignKey(Location)
    timeperiod = models.ForeignKey(TimePeriod)

    def __unicode__(self):
        return "[%s] %s-%s @%s" % (self.day, self.in_time, self.out_time, self.location)
