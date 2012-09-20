"""
tests review creation and viewing (validity and permissions)
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from people.models import *
import datetime
import pdb


class ReviewTestCase(TestCase):

    def setUp(self):
        """
        Preps the test db for permissions testing
        """
        self.dawg = User.objects.create_user('Dawg', 'dawg@test.com', 'pass')
        self.dawg.save()
        self.manager = User.objects.create_user('Manager', 'dawgm@test.com', 'pass')
        ct = ContentType.objects.get_for_model(UWLTReview)
        addReview = Permission.objects.get(content_type=ct, codename='add_uwltreview')
        finalize = Permission.objects.get(content_type=ct, codename='finalize_uwltreview')
        self.manager.user_permissions.add(addReview)
        self.manager.save()
        self.bigboss = User.objects.create_user('BigBoss', 'dawgb@test.com', 'pass')
        self.bigboss.user_permissions.add(addReview)
        self.bigboss.user_permissions.add(finalize)
        self.bigboss.save()
        d = datetime.date.today()
        self.dawgreview = UWLTReview.objects.create(user=self.dawg, date=d, reviewer=self.manager, dependability=3, productivity=4, customer_service=3, teamwork=4, integrity=5, technical_knowledge=3, attitude=5, responsibility=2, policies=4, communication=2, initiative=4, procedures=3)
        self.managerreview = UWLTReview.objects.create(user=self.manager, date=d, reviewer=self.bigboss, dependability=5, productivity=4, customer_service=5, teamwork=4, integrity=5, technical_knowledge=4, attitude=5, responsibility=4, policies=4, communication=4, initiative=4, procedures=3)
        self.bigbossreview = UWLTReview.objects.create(user=self.bigboss, date=d, reviewer=self.manager, dependability=5, productivity=4, customer_service=4, teamwork=4, integrity=5, technical_knowledge=5, attitude=5, responsibility=5, policies=4, communication=2, initiative=4, procedures=4)
        self.dawgprofile = UserProfile.objects.create(user=self.dawg)
        self.managerprofile = UserProfile.objects.create(user=self.manager)
        self.bigbossprofile = UserProfile.objects.create(user=self.bigboss)

    def testStaffPermissions(self):
        """
        Tests permissions for basic staff member
        """
        c = Client()
        c.login(username="Dawg", password='pass')
        resp3 = c.get('/people/Dawg/view_reviews/info/?id=1')
        self.assertEqual(resp3.status_code, 200)  # access to his own json review I guess
        resp4 = c.get('/people/Manager/view_reviews/info/?id=2')
        self.assertContains(resp4, "You do not have permission")  # no access to others jsons
        resp1 = c.get('/people/Dawg/view_reviews/')
        self.assertEqual(resp1.status_code, 200)
        self.assertContains(resp1, "Reviews for Dawg")
        resp = c.get('/people/Dawg/review/')
        self.assertContains(resp, "security hole")
        resp2 = c.get('/people/Manager/view_reviews/')
        self.assertContains(resp2, "security hole")  # change to 403 when we get django 1.4
        c.logout()

    def testManagerPermissions(self):
        """
        Tests permissions for someone who can add reviews but is
        not a superuser/final reviewer
        """
        c = Client()
        c.login(username="Manager", password='pass')
        resp1 = c.get('/people/Manager/view_reviews/')
        self.assertEqual(resp1.status_code, 200)
        self.assertContains(resp1, 'Reviews for Manager')
        resp2 = c.get('/people/Dawg/view_reviews/')
        self.assertEqual(resp2.status_code, 200)
        self.assertContains(resp2, 'security hole')
        resp = c.get('/people/Dawg/review/')
        self.assertEqual(resp.status_code, 200)
        resp3 = c.get('/people/BigBoss/view_reviews/')
        self.assertEqual(resp3.status_code, 200)
        self.assertContains(resp3, 'security hole')
        resp4 = c.get('/people/Manager/view_reviews/info/?id=2')
        self.assertEqual(resp4.status_code, 200)
        resp5 = c.get('/people/Dawg/view_reviews/info/?id=1')
        self.assertEqual(resp5.status_code, 200)
        self.assertContains(resp5, 'You do not have permission')
        c.logout()

    def testBigBossPermissions(self):
        """
        Tests permissions for superuser/final reviewer
        """
        c = Client()
        c.login(username="BigBoss", password='pass')
        resp1 = c.get('/people/Manager/view_reviews/')
        self.assertEqual(resp1.status_code, 200)
        resp = c.get('/people/Manager/review/')
        self.assertEqual(resp.status_code, 200)
        resp2 = c.get('/people/BigBoss/review/')
        self.assertEqual(resp2.status_code, 200)
        resp3 = c.get('/people/Dawg/view_reviews/info/?id=1')
        self.assertEqual(resp3.status_code, 200)
        resp4 = c.get('/people/BigBoss/view_reviews/info/?id=3')
        self.assertEqual(resp4.status_code, 200)
        c.logout()
