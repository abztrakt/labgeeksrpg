from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """ Defines additional things we should know about users.
    """
    user = models.ForeignKey(User, unique=True)
    hp = models.IntegerField()
    xp = models.IntegerField()
    currency = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    grad_date = models.DateField(null=True, blank=True)
    office = models.CharField(max_length=256, blank=True, default='')
    about_me = models.TextField(blank=True)
    phone = models.CharField(max_length=12, blank=True)
    alt_phone = models.CharField(max_length=12, blank=True)

