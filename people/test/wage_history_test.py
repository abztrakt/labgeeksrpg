"""
Tests creation, viewing of, and permssions for WageHistory object (and WageChangeReason)
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from people.models import *
import datetime
import pdb


class WageHistoryTestCase(TestCase):

    def setUp(self):
        """
        Preps the test db for permissions testing
        """
        self.dawg = User.objects.create_user('Dawg', 'dawg@test.com', 'pass')
        self.dawg.save()
        ct2 = ContentType.objects.get_for_model(WageHistory)
        viewHistory = Permission.objects.get(content_type=ct2, codename='view_wagehistory')
        self.bigboss = User.objects.create_user('BigBoss', 'dawgb@test.com', 'pass')
        self.bigboss.user_permissions.add(viewHistory)
        self.bigboss.save()
        d = datetime.date.today()
        self.hired = WageChangeReason.objects.create(title='Hired!')
        self.dawgwh = WageHistory.objects.create(user=self.dawg, effective_date=d, wage=11, wage_change_reason=self.hired)
        self.bigbosswh = WageHistory.objects.create(user=self.bigboss, effective_date=d, wage=20, wage_change_reason=self.hired)
        self.dawgprofile = UserProfile.objects.create(user=self.dawg)
        self.bigbossprofile = UserProfile.objects.create(user=self.bigboss)

    def test_staff_wage_history(self):
        """
        Tests permissions for basic staff member
        """
        c = Client()
        c.login(username="Dawg", password='pass')
        resp2 = c.get('/people/BigBoss/wage_history/')
        self.assertContains(resp2, "security hole")  # can't view other's wage history
        resp1 = c.get('/people/Dawg/wage_history/')
        self.assertEqual(resp1.status_code, 200)  # can view his own wage history
        c.logout()

    def test_BigBoss_wage_history(self):
        """
        Tests permissions for superuser/final reviewer
        """
        c = Client()
        c.login(username="BigBoss", password='pass')
        resp2 = c.get('/people/Dawg/wage_history/')
        self.assertEqual(resp2.status_code, 200)  # has the view histories permission
        resp2 = c.get('/people/BigBoss/wage_history/')
        self.assertEqual(resp2.status_code, 200)  # own wage history
        c.logout()
