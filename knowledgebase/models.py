from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Question(models.Model):
    """
    Question model that stores an issue that someone has.  There is no navigation to question, only search
    """
    question = models.CharField(max_length='200')
    more_info = models.TextField()
    user = models.ForeignKey(User, null=True)
    date = models.DateField()

    def __unicode__(self):
        return self.name


class Answer(models.Model):
    """
    Possible resolutions that have a foreignkey to the issue they claim to
    solve.  The best Answer will be selected by someone with the authority
    and is_best will be set to true.
    """
    answer = models.TextField()
    user = models.ForeignKey(User, null=True)
    date = models.DateField()
    question = models.ForeignKey(Question, null=True, blank=True)
    is_best = models.BooleanField(default=False)

    def __unicode__(self):
        return "Answer submitted by %s on %s" % (self.user, self.date)
