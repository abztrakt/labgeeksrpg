"""
Begin testing for Chronos, import proper libraries and models.
"""
from django.test import TestCase
from datetime import datetime
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.test.client import Client
from labgeeksrpg.schedule import models as p_models
from labgeeksrpg.schedule import views as p_views
from people.models import UserProfile


class StartTestCase(TestCase):
    """
    Create models for the test cases. Make sure all test cases inherit from this class so that they have models.
    Feel free to add or edit models.
    """
    def setUp(self):

        #Create users
        self.user1 = User.objects.create(username='user1', email='user1@uw.edu')
        self.user1.set_password('123')
        self.user2 = User.objects.create(username='user2')
        self.user1.save()
        self.user2.save()

        #Create user profiles
        self.user_profile1 = UserProfile.objects.create(user=self.user1)
        self.user_profile2 = UserProfile.objects.create(user=self.user2)
        self.user_profile1.save()
        self.user_profile2.save()


class TimePeriodTestCase(StartTestCase):
    """
    Test cases for the TimePeriod model.
    """

    def setUp(self):
        super(TimePeriodTestCase, self).setUp()

        # Create timeperiods.
        self.timeperiod1 = p_models.TimePeriod.objects.create(name='timeperiod1', slug='timeperiod1')
        self.timeperiod2 = p_models.TimePeriod.objects.create(name='timeperiod2', slug='timeperiod2')
        self.timeperiod1.save()
        self.timeperiod2.save()

    def test_empty_working_periods(self):
        user_profile1 = self.user_profile1
        user_profile2 = self.user_profile2
        timeperiod1 = self.timeperiod1
        timeperiod2 = self.timeperiod2

        # Make sure that nobody at this point chose a timeperiod.
        working_periods1 = user_profile1.working_periods.all()
        working_periods2 = user_profile2.working_periods.all()
        self.assertFalse(working_periods1)
        self.assertFalse(working_periods1)

    def test_working_periods(self):
        self.client = Client()
        self.client.login(username='user1', password='123')
        response = self.client.post('/schedule/timeperiods/', {'user': 'user1', 'timeperiods': 'timeperiod1'})
        timeperiods = p_models.TimePeriod.objects.all()
        self.assertTrue(response.context['timeperiods'][0] in timeperiods)
        self.assertEqual(self.user_profile1.working_periods.all(), response.context['timeperiods'])
