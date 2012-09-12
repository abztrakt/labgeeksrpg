'''
tests answer creation and selection
'''

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, Permission
from delphi.models import *
from django.contrib.contenttypes.models import ContentType
import datetime
import pdb


class AnswerTestCase(TestCase):

    def setUp(self):
        self.dawg = User.objects.create_user('Dawg', 'dawg@test.com', 'pass')
        self.dawg.save()
        answer = ContentType.objects.get_for_model(Answer)
        question = ContentType.objects.get_for_model(Question)
        can_answer = Permission.objects.get(content_type=question, codename='can_answer')
        select_answer = Permission.objects.get(content_type=answer, codename='can_select_answer')
        self.boss = User.objects.create_user('Boss', 'boss@test.com', 'pass')
        self.boss.user_permissions.add(select_answer, can_answer)
        self.boss.save()
        self.answerman = User.objects.create_user('AnswerMan', 'answerman@test.com', 'pass')
        self.answerman.user_permissions.add(can_answer)
        self.answerman.save()
        Question.objects.create(question='How do I internet?', more_info='I cannot internet. How do I internet? herpderp', user=self.dawg, date=datetime.date.today())

    def testAnswers(self):
        client = Client()
        client.login(username='Dawg', password='pass')
        resp = client.get('/delphi/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'herpderp')
        resp = client.get('/delphi/1/answer/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'security hole')
        client.logout()
        client.login(username='AnswerMan', password='pass')
        resp = client.get('/delphi/1/answer/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Answering question')
        resp = client.post('/delphi/1/answer/', {'answer': 'With your brain'})
        self.assertEqual(resp.status_code, 302)
        resp = client.get('/delphi/1/')
        self.assertContains(resp, 'With your brain')
        self.assertContains(resp, 'no best solution')
        resp = client.get('/delphi/1/select_answer/?id=1')
        self.assertContains(resp, 'security hole')
        client.logout()
        client.login(username='Boss', password='pass')
        resp = client.get('/delphi/1/answer/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Answering question')
        resp = client.post('/delphi/1/answer/', {'answer': 'Click on your browser first'})
        self.assertEqual(resp.status_code, 302)
        resp = client.get('/delphi/1/')
        self.assertContains(resp, 'on your browser')
        self.assertContains(resp, 'no best solution')
        resp = client.get('/delphi/1/select_answer/?id=1')
        answer1 = Answer.objects.get(id=1)
        answer2 = Answer.objects.get(id=2)
        self.assertEqual(answer1.is_best, True)
        self.assertEqual(answer2.is_best, False)
        resp = client.get('/delphi/1/select_answer/?id=1&id=2')
        self.assertEqual(resp.status_code, 302)
        answer1 = Answer.objects.get(id=1)
        answer2 = Answer.objects.get(id=2)
        self.assertEqual(answer1.is_best, True)
        self.assertEqual(answer2.is_best, True)
        resp = client.get('/delphi/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'answers yet')
        resp = client.get('/delphi/1/select_answer/?id=2')
        answer1 = Answer.objects.get(id=1)
        answer2 = Answer.objects.get(id=2)
        self.assertEqual(answer1.is_best, False)
        self.assertEqual(answer2.is_best, True)
        resp = client.get('/delphi/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'other solutions')
        self.assertContains(resp, 'Best solutions')
        client.logout()
