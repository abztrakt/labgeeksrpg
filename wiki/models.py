from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Page(models.Model):
    """basic Page model for the wiki"""
    name = models.CharField(max_length='25')
    content = models.TextField()
    author = models.ForeignKey(User, null=True, blank=True)
    date = models.DateField(default=date.today, null=True)

    def __unicode__(self):
        return self.name
