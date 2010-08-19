from django.db import models
from django.contrib.auth.models import User
import datetime

class Player(models.Model):
    """ Defines additional skills, knowledge, etc. regarding staff members
    """
    user = models.ForeignKey(User, unique=True)
    hp = models.IntegerField()
    xp = models.IntegerField()
    currency = models.IntegerField()
    avatar = models.ImageField(upload_to = "images/%Y/%m/%d", null=True, blank=True)
    seniority = models.IntegerField()

    def __unicode__(self):
        return "%s %s [%s]" % (self.user.first_name, self.user.last_name, self.user.username)

class Pay_grade(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name

class Review(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, related_name="review_user")
    manager = models.ForeignKey(User, related_name="review_manager")
    notes = models.TextField()

    def __unicode__(self):
        return "%s on %s" % (self.user, self.date) 
