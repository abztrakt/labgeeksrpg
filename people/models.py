from django.db import models
from datetime import date
from django.contrib.auth.models import User

class EmploymentStatus(models.Model):
    """ Defines statuses that a Person could hold.
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

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

class WorkGroup(models.Model):
    """ Defines which team the person is on.
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class PayGrade(models.Model):
    """ A tier for a position which determines the wage.
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    wage = models.FloatField()

    def __unicode__(self):
        return self.name

class Title(models.Model):
    """ Provides a relation between WorkGroups and PayGrades.
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    description = models.TextField()
    workgroup = models.ForeignKey(WorkGroup)
    pay_grade = models.ForeignKey(PayGrade)

    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    """ Defines additional things we should know about users.
    """
    user = models.ForeignKey(User, unique=True, related_name='uwnetid')
    staff_photo = models.ImageField(upload_to="images/%Y/%m/%d", null=True, blank=True)
    badge_photo = models.ImageField(upload_to="images/%Y/%m/%d", null=True, blank=True)
    call_me_by = models.CharField(max_length=256, null=True, blank=True)
    status = models.ForeignKey(EmploymentStatus, null=True, blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    grad_date = models.DateField(null=True,blank=True)
    supervisor = models.ForeignKey(User, related_name='supervisor', null=True, blank=True)
    title = models.ForeignKey(Title, null=True, blank=True)
    office = models.CharField(max_length=256, null=True, blank=True, default='')
    working_periods = models.ManyToManyField(TimePeriod, null=True, blank=True)
    about_me = models.TextField(null=True,blank=True)
    phone = models.CharField(max_length=12, null=True,blank=True)
    alt_phone = models.CharField(max_length=12, null=True, blank=True)
    site_skin = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return "%s %s [%s]" % (self.user.first_name, self.user.last_name, self.user.username)
