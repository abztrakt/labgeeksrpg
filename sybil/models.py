from django.db import models
from haystack.models import *
from django.contrib.auth.models import User


class Screenshot(models.Model):
    picture = models.ImageField(upload_to='oracles/screenshots/', null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    date = models.DateField(null=True)
    name = models.CharField(null=True, max_length=50)

    def __unicode__(self):
        return str(self.pk)


class Tag(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()

    def __unicode__(self):
        return self.name
