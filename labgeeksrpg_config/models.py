from django.db import models

class Notification(models.Model):
    date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=256)

    def __unicode__(self):
        return self.title

