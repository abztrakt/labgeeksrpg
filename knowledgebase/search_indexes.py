import datetime
from haystack.indexes import *
from haystack import site
from knowledgebase.models import Answer

class AnswerIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    question = CharField(model_attr='question', null=True)
    user = CharField(model_attr='user', null=True)
    date = DateTimeField(model_attr='date')

    content_auto = EdgeNgramField(model_attr='content')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Answer.objects.filter(date__lte=datetime.datetime.now())

site.register(Answer, AnswerIndex)
