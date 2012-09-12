'''
Tests creation of questions
'''

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from delphi.models import *
import datetime
import pdb


class QuestionTestCase(TestCase):

    def setUp(self):
        self.dawg = User.objects.create_user('Dawg', 'dawg@test.com', 'pass')
        self.dawg.save()
        self.dawg2 = User.objects.create_user('Dawg2', 'dawg2@test.com', 'pass')
        self.dawg2.save()

    def testQuestion(self):
        client = Client()
        client.login(username='Dawg', password='pass')
        resp = client.get('/delphi/create/')
        self.assertEqual(resp.status_code, 200)
        resp = client.post('/delphi/create/', {'question': 'How do I internet?', 'more_info': 'I cannot internet.  How do I internet?  herpderp'})
        self.assertEqual(resp.status_code, 302)
        resp = client.get('/delphi/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'herpderp')
        client.logout()
        client.login(username='Dawg2', password='pass')
        resp = client.get('/delphi/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'herpderp')
        resp = client.get('/delphi/create/')
        self.assertEqual(resp.status_code, 200)
        resp = client.post('/delphi/create/', {'question': 'How do I become less of a noob?', 'more_info': 'My name is Noobert Ownian'})
        self.assertEqual(resp.status_code, 302)
        resp = client.get('/delphi/2/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Noobert Ownian')
        client.logout()
