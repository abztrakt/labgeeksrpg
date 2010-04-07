from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

class Punchclock(models.Model):
    name = models.CharField(max_length=256)
    location = models.ForeignKey(Location)
    ip_address = models.IPAddressField()

    def __unicode__(self):
        return self.name

class Shift(models.Model):
    person = models.ForeignKey(User)
    intime = models.DateTimeField()
    outtime = models.DateTimeField(blank=True, null=True)
    punchclock = models.ForeignKey(Punchclock)
    shiftnote = models.TextField(blank=True)

    def __unicode__(self):
        return "%s@[%s]-[%s]" % (self.person, self.intime, self.outtime)
