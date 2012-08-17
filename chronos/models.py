from django.db import models
from django.contrib.auth.models import User
import datetime


class Location(models.Model):
    """ The location of the punchclock, as well as the location staff are
    signing in for. This lets us use multiple computers on site as punchclocks.
    """
    name = models.CharField(max_length=256)
    active_users = models.ManyToManyField(User, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Punchclock(models.Model):
    """ The computer we'll check ip address against to make sure staff are
    allowed to sign in from here.
    """
    name = models.CharField(max_length=256)
    location = models.ForeignKey(Location)
    ip_address = models.IPAddressField()

    def __unicode__(self):
        return self.name


class Shift(models.Model):
    """ The shift the user is signing into or out of. A historical record of a
    work session.
    """
    person = models.ForeignKey(User)
    intime = models.DateTimeField()
    outtime = models.DateTimeField(blank=True, null=True)
    in_clock = models.ForeignKey(Punchclock, related_name="in_punchclock", null=True, blank=True)
    out_clock = models.ForeignKey(Punchclock, related_name="out_punchclock", null=True, blank=True)
    shiftnote = models.TextField(blank=True)

    def length(self):
        """ Returns the length of a shift in hours.
        """
        if self.outtime:
            delta = self.outtime - self.intime
            seconds = float((delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 10 ** 6) / 10 ** 6)
            hours = float(seconds / 60 / 60)
            return "%.02f" % hours
        else:
            return datetime.timedelta(0)

    def __unicode__(self):
        return "%s@[%s]-[%s]" % (self.person, self.intime, self.outtime)
