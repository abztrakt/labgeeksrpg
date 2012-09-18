from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Page(models.Model):
    """basic Page model for the wiki"""
    name = models.CharField(max_length='50')
    slug = models.SlugField(unique=True, null=True)
    content = models.TextField()
    author = models.ForeignKey(User, null=True, blank=True)
    date = models.DateField(null=True)
    times_viewed = models.IntegerField(null=True, default=0)
    tags = models.ManyToManyField('sybil.Tag', null=True)

    def __unicode__(self):
        return self.name


class RevisionHistory(models.Model):
    after = models.TextField()
    page = models.ForeignKey(Page)
    user = models.ForeignKey(User)
    date = models.DateField()
    notes = models.CharField(null=True, max_length='260')

    def __unicode__(self):
        return "%s - %s on %s: %s" % (self.page, self.user, self.date, self.notes)
