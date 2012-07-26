"""
Tests creation, veiwing and editing (and permissions) of profiles
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from people.models import *
import datetime
import pdb


class ProfileTestCase(TestCase):

    def setUp(self):
        """
        Preps the test
        """
        self.dawg = User.objects.create_user('Dawg', 'dawg@test.com', 'pass')
        self.dawg.save()
        self.dawg2 = User.objects.create_user('Dawg2', 'dawg@test.com', 'pass')
        self.dawg2.save()
        self.manager = User.objects.create_user('Manager', 'dawgm@test.com', 'pass')
        ct = ContentType.objects.get_for_model(UserProfile)
        addProfile = Permission.objects.get(content_type=ct, codename='add_userprofile')
        editProfile = Permission.objects.get(content_type=ct, codename='change_userprofile')
        self.manager.user_permissions.add(editProfile)
        self.manager.save()
        self.bigboss = User.objects.create_user('BigBoss', 'dawgb@test.com', 'pass')
        self.bigboss.user_permissions.add(addProfile)
        self.bigboss.user_permissions.add(editProfile)
        self.bigboss.save()
        self.managerprofile = UserProfile.objects.create(user=self.manager)
        self.dawg2profile = UserProfile.objects.create(user=self.dawg2)

    def testStaffProfilePermissions(self):
        """
        Tests permissions for basic staff member
        """
        c = Client()
        c.login(username="Dawg", password='pass')
        resp1 = c.get('/people/Manager/')
        self.assertEqual(resp1.status_code, 200)  # access to created profiles
        resp2 = c.get('/people/Dawg/')
        self.assertEqual(resp2.status_code, 200)  # can create his own profile
        resp3 = c.get('/people/Manager/edit/')
        self.assertContains(resp3, 'Sorry')  # can't edit other profiles
        resp4 = c.get('/people/BigBoss/')
        self.assertContains(resp4, 'Sorry')  # can't add other profiles
        c.logout()
        c.login(username='Dawg2', password='pass')
        resp5 = c.get('/people/Dawg2/edit/')
        self.assertContains(resp5, 'You are editing')  # can edit own profile
        c.logout()

    def testManagerProfilePermissions(self):
        """
        Tests permissions for someone who can add profiles
        """
        c = Client()
        c.login(username="Manager", password='pass')
        resp1 = c.get('/people/Dawg2/')
        self.assertEqual(resp1.status_code, 200)  # access to created profiles
        resp2 = c.get('/people/Manager/edit/')
        self.assertContains(resp2, "You are editing")  # can edit his own profile
        resp3 = c.get('/people/Dawg2/edit/')
        self.assertContains(resp3, 'You are editing')  # can edit other profiles
        resp4 = c.get('/people/BigBoss/')
        self.assertContains(resp4, 'Sorry')  # can't add other profiles
        c.logout()

    def testBigBossProfilePermissions(self):
        """
        Tests permissions for someone with editing power
        """
        c = Client()
        c.login(username="BigBoss", password='pass')
        resp1 = c.get('/people/Dawg2/')
        self.assertEqual(resp1.status_code, 200)  # access to created profiles
        resp2 = c.get('/people/BigBoss/')
        self.assertContains(resp2, "You are creating")  # can edit/create his own profile
        resp3 = c.get('/people/Dawg2/edit/')
        self.assertContains(resp3, 'You are editing')  # can edit other profiles
        resp4 = c.get('/people/Dawg/')
        self.assertContains(resp4, 'You are creating')  # can add other profiles
        c.logout()
