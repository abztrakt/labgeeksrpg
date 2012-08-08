"""
Begin testing for Chronos, import proper libraries and models.
"""
from django.test import TestCase
from datetime import datetime
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from labgeeksrpg.chronos import models as c_models
from labgeeksrpg.chronos import views as c_views


class StartTestCase(TestCase):
    """
    Create models for the test cases. Make sure all test cases inherit from this class so that they have models.
    Feel free to add or edit models.
    """
    def setUp(self):

        #Create users and set permissions
        self.ryu = User.objects.create(username='Ryu', password='hadouken', email='ryu@streetfighter.com')
        self.ken = User.objects.create(username='Ken', password='shoryuken', email='ken@streetfighter.com')
        self.akuma = User.objects.create(username='Akuma', password='shun goku satsu', email='akuma@streetfighter.com')

        # Ryu can do anything an admin can do.
        self.ryu.is_active = True
        self.ryu.is_staff = True
        self.ryu.is_superuser = True

        # Ken can do anything a regular staff can do, minus things a superuser user can do.
        self.ken.is_active = True
        self.ken.is_staff = True
        self.ken.is_superuser = False

        # Akuma is no longer staff, and has no permissions.
        self.akuma.is_active = False
        self.akuma.is_staff = False
        self.akuma.is_superuser = False

        #Create locations. These are used for clocking in and out
        self.loc1 = c_models.Location.objects.create(name='Japan')
        self.loc2 = c_models.Location.objects.create(name='America')
        self.loc3 = c_models.Location.objects.create(name='Japan')

        #Ip addresses, used for verifying punchclock locations
        self.ip1 = '000.000.00.00'
        self.ip2 = '123.456.78.90'
        self.ip3 = '111.222.33.44'

        #Punch clocks, where people can clock in.
        self.pc1 = c_models.Punchclock.objects.create(name='Rooftop', location=self.loc1, ip_address=self.ip1)
        self.pc2 = c_models.Punchclock.objects.create(name='Harbor', location=self.loc2, ip_address=self.ip2)
        self.pc3 = c_models.Punchclock.objects.create(name='Temple', location=self.loc3, ip_address=self.ip3)
        #Imitate a HTMLrequest object
        self.request = self.client

        #Save the fields to the test db to imitate the live site data.
        self.ryu.save()
        self.ken.save()
        self.akuma.save()
        self.loc1.save()
        self.loc2.save()
        self.loc3.save()
        self.pc1.save()
        self.pc2.save()
        self.pc3.save()


class ModelsTestCase(StartTestCase):
    """
    Test the models for Chronos. Add / edit any test.
    """
    def test_location(self):
        #Should be true
        self.assertEqual(self.loc1.name, 'Japan')
        self.assertEqual(self.loc2.name, 'America')
        self.assertEqual(self.loc3.name, 'Japan')

    def test_punchclock(self):
        #Should be true
        self.assertEqual(self.pc1.location.name, 'Japan')
        self.assertNotEqual(self.pc2.location, 'Japan')
        self.assertIsNotNone(c_models.Punchclock.objects.get(name='Rooftop'))


class ClockInClockOutTestCase(StartTestCase):
    """
    Test if users are properly clocking in and out.
    """
    def test_clockin(self):
        #self.request.method = 'POST'
        pass


class ShiftsTestCase(StartTestCase):

    """
    Test shifts. Make sure we are grabbing the right ones. Either create shifts or use ones from the db.
    """
    def setUp(self):
        super(ShiftsTestCase, self).setUp()
        person = self.ryu
        intime = datetime(2011, 1, 1, 8, 0)
        shift = c_models.Shift(person=person, intime=intime)
        shift.save()

    def test_get_correct_shifts(self):
        year = 2011
        month = 1
        day = 1
        user = self.ryu
        week = 1
        payperiod = 1

        self.assertIsNotNone(c_views.get_shifts(year, month, day, user, week, payperiod))
        self.assertIsNotNone(c_views.get_shifts(year, month, None, None, None, None))
