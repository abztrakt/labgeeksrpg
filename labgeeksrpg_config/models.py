from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Notification(models.Model):
    date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=256, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, editable=False, null=True, blank=True)
    archived = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title
