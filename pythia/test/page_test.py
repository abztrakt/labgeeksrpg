"""
Tests creation and editing of pages
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from pythia.models import *
import datetime
import pdb


class PageTestCase(TestCase):

    def setUp(self):
        '''
        PREP!
        '''
        self.dawg = User.objects.create_user('Dawg', 'dawg@test.com', 'pass')
        self.dawg.save()
        self.writer = User.objects.create_user('Writer', 'writer@test.com', 'pass')
        self.editor = User.objects.create_user('Editor', 'editor@test.com', 'pass')
        page = ContentType.objects.get_for_model(Page)
        add_page = Permission.objects.get(content_type=page, codename='add_page')
        edit_page = Permission.objects.get(content_type=page, codename='change_page')
        self.writer.user_permissions.add(add_page)
        self.writer.save()
        self.editor.user_permissions.add(add_page, edit_page)
        self.editor.save()
        hello = Page.objects.create(name='Hello', slug='hello', content='empty', date=datetime.date.today(), author=self.writer)
        RevisionHistory.objects.create(after='empty', user=self.writer, date=datetime.date.today(), page=hello, notes='initial')

    def testPageCreation(self):
        client = Client()
        client.login(username='Dawg', password='pass')
        resp = client.get('/pythia/create_page/')
        self.assertContains(resp, 'Without your space helmet')
        client.logout()
        client.login(username='Writer', password='pass')
        resp = client.get('/pythia/create_page/')
        self.assertContains(resp, 'Create Page')
        resp = client.post('/pythia/None/edit/', {'content': 'I am a wee babby wiki page', 'notes': 'inintial page creation', 'page_name': "I'm a page!"})
        self.assertEqual(resp.status_code, 302)  # will be a redirect if successful
        resp = client.get('/pythia/im-a-page/')  # testing slugification along with page creation
        self.assertEqual(resp.status_code, 200)
        client.logout()

    def testPageEditing(self):
        client = Client()
        client.login(username='Dawg', password='pass')
        resp = client.get('/pythia/hello/')
        self.assertContains(resp, 'empty')
        resp = client.get('/pythia/hello/edit/')
        self.assertContains(resp, 'Without your space helmet')
        client.logout()
        client.login(username='Writer', password='pass')
        resp = client.get('/pythia/hello/edit/')
        self.assertContains(resp, 'Without your space helmet')
        client.logout()
        client.login(username='Editor', password='pass')
        resp = client.get('/pythia/hello/edit/')
        self.assertContains(resp, 'Edit Page')
        resp = client.post('/pythia/hello/edit/', {'content': 'This is NOT an empty page.  I swear', 'notes': 'not empty', 'page_name': 'hello'})
        self.assertEqual(resp.status_code, 302)  # will be a 'found' redirect
        resp = client.get('/pythia/hello/')
        self.assertContains(resp, 'This is NOT an empty page.')
