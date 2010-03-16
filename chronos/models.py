from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    name = models.CharField(max_length=256)

class Punchclock(models.Model):
    name = models.CharField(max_length=256)
    location = models.ForeignKey(Location)
    ip_address = models.IPAddressField()

class Shift(models.Model):
    person = models.ForeignKey(User)
    intime = models.DateTimeField()
    outtime = models.DateTimeField()
    punchclock = models.ForeignKey(Punchclock)
