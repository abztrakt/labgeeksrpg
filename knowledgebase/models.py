from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Issue(models.Model):
    """
    Issue model that stores and issue and has a foreignkey to a resolution
    """
    name = models.CharField(max_length='30')
    content = models.TextField()
    user = models.ForeignKey(User, null=True)
    chosen_resolution = models.ForeignKey('Resolution', related_name="%(app_label)s_%(class)s_related", null=True, blank=True)
    date = models.DateField()

    def __unicode__(self):
        return self.name


class Resolution(models.Model):
    """
    Possible resolutions that have a foreignkey to the issue they claim to
    solve.  The issue will point to the best resolution as selected by a lead
    """
    content = models.TextField()
    user = models.ForeignKey(User, null=True)
    date = models.DateField()
    issue = models.ForeignKey(Issue, null=True, blank=True)

    def __unicode__(self):
        return "Resolution submitted by %s on %s" % (self.user, self.date)
