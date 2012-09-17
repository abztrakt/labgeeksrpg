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


class RevisionHistoryTestCase(TestCase):

    def setUp(self):
        '''
        PREP!
        '''
        self.dawg = User.objects.create_user('Dawg', 'dawg@test.com', 'pass')
        self.dawg.save()
        self.writer = User.objects.create_user('Writer', 'writer@test.com', 'pass')
        self.editor = User.objects.create_user('Editor', 'editor@test.com', 'pass')
        RH = ContentType.objects.get_for_model(RevisionHistory)
        page = ContentType.objects.get_for_model(Page)
        edit_page = Permission.objects.get(content_type=page, codename='change_page')
        change_revisionhistory = Permission.objects.get(content_type=RH, codename='change_revisionhistory')
        self.writer.user_permissions.add(change_revisionhistory)
        self.writer.save()
        self.editor.user_permissions.add(edit_page, change_revisionhistory)
        self.editor.save()

    def testRevisionHistory(self):
        hello = Page.objects.create(name='Hello', slug='hello', content='empty', date=datetime.date.today(), author=self.writer)
        RevisionHistory.objects.create(after='empty', user=self.writer, date=datetime.date.today(), page=hello, notes='initial')
        client = Client()
        client.login(username='Editor', password='pass')
        resp = client.get('/pythia/hello/edit/')
        self.assertContains(resp, 'Edit Page')
        resp = client.post('/pythia/hello/edit/', {'content': 'This is a full page.  I swear', 'notes': 'not empty', 'page_name': 'hello'})
        self.assertEqual(resp.status_code, 302)  # will be a 'found' redirect
        resp = client.get('/pythia/hello/')
        self.assertContains(resp, 'This is a full page.')  # testing to see if page changed
        revisions = RevisionHistory.objects.filter(page=hello)
        self.assertEqual(len(revisions), 2)
        resp = client.post('/pythia/hello/select_revision/', {'id': 1})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'empty')  # revision is properly selected
        revision = RevisionHistory.objects.get(id=1)
        resp = client.post('/pythia/hello/edit/', {'content': revision.after, 'page_name': 'hello', 'notes': 'test rollback'})
        self.assertEqual(resp.status_code, 302)
        resp = client.get('/pythia/hello/')
        self.assertContains(resp, 'empty')  # revision is properly applied
        revisions = RevisionHistory.objects.filter(page=hello)
        self.assertEqual(len(revisions), 3)  # RevisionHistory object created
        resp = client.post('/pythia/hello/select_revision/', {'id': 1})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'empty')  # revision is properly selected
        revision = RevisionHistory.objects.get(id=1)
        resp = client.post('/pythia/hello/edit/', {'content': revision.after, 'page_name': 'hello', 'notes': 'test rollback'})
        self.assertEqual(resp.status_code, 302)
        resp = client.get('/pythia/hello/')
        self.assertContains(resp, 'empty')  # content is the same as before
        self.assertEqual(len(revisions), 3)  # no new Revisionhistory object created
