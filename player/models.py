from django.db import models

class Player(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    uwnetid = models.CharField(max_length=8)
# TODO: what is an appropriate field type for the points?
    xp = models.CharField(max_length=5)
    currency = models.CharField(max_length=5)
# TODO: make status another model so statuses can be added/changed
    status = models.CharField(max_length=25)

#TODO: implement an algorithm to return player's level based on xp
    def level():
        pass

    def __unicode__(self):
        return self.uwnetid

class Skills(models.Model):
    pass
