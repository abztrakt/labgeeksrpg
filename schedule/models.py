from django.db import models
from django.contrib.auth.models import User
from labgeeksrpg.chronos.models import Location
import datetime

class WorkShift(models.Model):
    """ These are shifts that people are expected to work for. 
    """
    person = models.ForeignKey(User, null=True, blank=True)
    scheduled_in = models.DateTimeField()
    scheduled_out = models.DateTimeField()
    location = models.ForeignKey(Location)

    def __unicode__(self):
        return "%s: [%s] %s-%s @%s" % (self.person,self.scheduled_in.date(),self.scheduled_in.time(),self.scheduled_out.time(), self.location)
