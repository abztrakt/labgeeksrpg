from django.db import models

class Player(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    uwnetid = models.CharField(max_length=8)
# TODO: what is an appropriate field type for the points?
    hp = models.IntegerField()
    xp = models.IntegerField()
    currency = models.IntegerField()
# TODO: make status another model so statuses can be added/changed
    status = models.CharField(max_length=25)
    start_date = models.DateField()
    end_date = models.DateField(blank=True)
    grad_date = models.DateField()
# Phone numbers
    phone = models.CharField(max_length=10)
    alt_phone = models.CharField(max_length=10)
# Chat accounts
    uw_gmail = models.EmailField(max_length=75, blank=True)
    uw_windows_live = models.EmailField(max_length=75, blank=True)
    gmail = models.EmailField(max_length=75, blank=True)
    windows_live = models.EmailField(max_length=75, blank=True)
    aim_iChat = models.CharField(max_length=75, blank=True)
    irc_nick = models.CharField(max_length=75, blank=True)
    irc_network = models.CharField(max_length=75, blank=True)
    skype = models.CharField(max_length=75, blank=True)
    yahoo = models.EmailField(max_length=75, blank=True)

#TODO: implement the 'staff_photo = models.ImageField()'
    

#TODO: implement an algorithm to return player's level based on xp
    def level():
        pass

    def __unicode__(self):
        return self.uwnetid

class PlayerReview(models.Model):
    pass

class PlayerWageHistory(models.Model):
    pass

class Skills(models.Model):
#See whiteboard captures for ideas
    pass

class Position(models.Model):
#Attributes will be: Team, Title, Rank
#Possible sub-options: Commentor, Consultant, Senior Consultant, Lead, Senior Lead, Developer, Instructor, Rookie, Manager, PC Lead, Mac Lead, Network Lead
#Teams are: iTeam, Web Team, DS Team, Catalyst, Help Desk
    pass
