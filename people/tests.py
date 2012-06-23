"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from people.models import *
import datetime
import pdb


class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)


class PeopleTestCase(TestCase):

    def setUp(self):
        """
        Preps the test db for permissions testing
        """
        self.dawg = User.objects.create_user('Dawg', 'dawg@test.com', 'pass')
        self.dawg.save()
        self.manager = User.objects.create_user('Manager', 'dawgm@test.com', 'pass')
        ct = ContentType.objects.get_for_model(UWLTReview)
        permission = Permission.objects.get(content_type=ct, codename='add_uwltreview')
        self.manager.user_permissions.add(permission)
        self.manager.save()
        self.bigboss = User.objects.create_user('BigBoss', 'dawgb@test.com', 'pass')
        self.bigboss.is_superuser = True
        self.bigboss.save()
        d = datetime.date.today()
        self.dawgreview = UWLTReview.objects.create(user=self.dawg, date=d, reviewer=self.manager)
        self.managerreview = UWLTReview.objects.create(user=self.manager, date=d, reviewer=self.bigboss)
        self.bigbossreview = UWLTReview.objects.create(user=self.bigboss, date=d, reviewer=self.bigboss)
        self.dawgprofile = UserProfile.objects.create(user=self.dawg)
        self.managerprofile = UserProfile.objects.create(user=self.manager)

    def testStaffPermissions(self):
        """
        Tests permissions for basic staff member
        """
        c = self.client
        resp = c.get('/people/')
        self.assertEqual(resp.status_code, 302)
        self.client.login(username="Dawg", password='pass')
        resp1 = c.get('/people/')
        self.assertEqual(resp1.status_code, 200)
        resp2 = c.get('/people/Dawg/review/#view_reviews')
        self.assertEqual(resp2.status_code, 200)
        resp3 = c.get('/people/Manager/review/#view_reviews')
        self.assertEqual(resp3.status_code, 200)  # change to 403 when we get django 1.4
        resp4 = c.get('/people/Manager/#profile')
        self.assertEqual(resp4.status_code, 200)  # access to created profiles
        c.logout()

    def testManagerPermissions(self):
        """
        Tests permissions for someone who can add reviews but is
        not a superuser/final reviewer
        """
        c = self.client
        resp = c.get('/people/')
        self.assertEqual(resp.status_code, 302)
        c.login(username="Manager", password='pass')
        resp1 = c.get('/people/')
        self.assertEqual(resp1.status_code, 200)
        resp3 = c.get('/people/Manager/review/#view_reviews')
        self.assertEqual(resp3.status_code, 200)
        resp2 = c.get('/people/Dawg/review/#view_reviews')
        self.assertEqual(resp2.status_code, 200)
        resp4 = c.get('/people/Dawg/#profile')
        self.assertEqual(resp4.status_code, 200)
        resp5 = c.get('/people/BigBoss/review/#view_reviews')
        self.assertEqual(resp5.status_code, 200)  # change to 403 upon django 1.4 update
        c.logout()

    def testBigBossPermissions(self):
        """
        Tests permissions for superuser/final reviewer
        """
        c = self.client
        resp = c.get('/people/')
        self.assertEqual(resp.status_code, 302)
        c.login(username="BigBoss", password='pass')
        resp1 = c.get('/people/')
        self.assertEqual(resp1.status_code, 200)
        resp3 = c.get('/people/Manager/review/#view_reviews')
        self.assertEqual(resp3.status_code, 200)
        resp4 = c.get('/people/Dawg/#profile')
        self.assertEqual(resp4.status_code, 200)
        resp5 = c.get('/people/BigBoss/review/#view_reviews')
        self.assertEqual(resp5.status_code, 200)
        c.logout()
