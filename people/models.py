from django.db import models
from django.contrib.auth.models import User

class EmploymentStatus(models.Model):
    """ Defines statuses that a Person could hold.
    """
    slug = models.SlugField()
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)

class TimePeriod(models.Model):
    """ Defines possible periods of time when a person could choose to work or choose not to work.
    """
    slug = models.SlugField()
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)

class WorkGroup(models.Model):
    """ Defines which team the person is on.
    """
    slug = models.SlugField()
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)

class UserProfile(models.Model):
    """ Defines additional things we should know about users.
    """
    user = models.ForeignKey(User, unique=True, related_name='uwnetid')
    staff_photo = models.ImageField(upload_to="images/%Y/%m/%d", null=True, blank=True)
    call_me_by = models.CharField(max_length=256, blank=True)
    status = models.ForeignKey(EmploymentStatus)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    grad_date = models.DateField(null=True, blank=True)
    supervisor = models.ForeignKey(User, related_name='supervisor')
    title = models.CharField(max_length=256, blank=True) #To be made automagic later?
    office = models.CharField(max_length=256, blank=True, default='')
    working_periods = models.ForeignKey(TimePeriod)
    about_me = models.TextField(blank=True)
    phone = models.CharField(max_length=12, blank=True)
    alt_phone = models.CharField(max_length=12, blank=True)

    def __unicode__(self):
        return "%s %s [%s]" % (self.user.first_name, self.user.last_name, self.user.username)
