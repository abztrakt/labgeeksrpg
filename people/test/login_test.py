"""
tests login, logout and false login
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, Permission
from people.models import *
import datetime
import pdb


class LoginTestCase(TestCase):

    def setUp(self):
        """
        Preps the test db for permissions testing
        """
        self.dawg = User.objects.create_user('Dawg', 'dawg@test.com', 'pass')
        self.dawg.save()

    def testLoginRequired(self):
        """
        Tests permissions for basic staff member
        """
        c = Client()
        resp = c.get('/people/')
        self.assertEqual(resp.status_code, 302)  # not logged in yet
        c.login(username="Dawg", password='pass')
        resp1 = c.get('/people/')
        self.assertEqual(resp1.status_code, 200)  # successfully logged in
        c.logout()
        resp = c.get('/people/')
        self.assertEqual(resp.status_code, 302)  # logged back out
        c.login(username="Dog", password='pass')
        resp = c.get('/people/')
        self.assertEqual(resp.status_code, 302)  # bad username
        c.logout()
        c.login(username="Dawg", password='ass')
        resp1 = c.get('/people/')
        self.assertEqual(resp1.status_code, 302)  # bad password
        c.logout()
