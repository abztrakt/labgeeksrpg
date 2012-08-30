import datetime
from haystack.indexes import *
from haystack import site
from knowledgebase.models import Question, Answer

class QuestionIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    user = CharField(model_attr='user', null=True)
    date = DateTimeField(model_attr='date')

    def index_queryset(self):
        """Used when the entire index for model is updated"""
        return Question.objects.filter(date__lte=datetime.datetime.now())

class AnswerIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    user = CharField(model_attr='user', null=True)
    date = DateTimeField(model_attr='date')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Answer.objects.filter(date__lte=datetime.datetime.now())

site.register(Question, QuestionIndex)
site.register(Answer, AnswerIndex)
