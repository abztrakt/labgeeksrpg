from labgeeksrpg.delphi.models import *
from django import forms
from django.forms import ModelForm


class CreateQuestionForm(ModelForm):
    """
    Handles the creation of questions that need answers
    """
    question = forms.CharField(max_length='100', help_text='What is your question?', required=True)
    more_info = forms.CharField(widget=forms.Textarea, help_text='Describe your issue in detail:', required=True)

    class Meta:
        model = Question
        fields = ('question', 'more_info',)

    def save(self, *args, **kwargs):
        inst = ModelForm.save(self, *args, **kwargs)
        return inst


class CreateAnswerForm(ModelForm):
    """
    Handles the creation of an answer to a question
    """
    answer = forms.CharField(widget=forms.Textarea, help_text='Answer this question below:', required=True)

    class Meta:
        model = Answer
        fields = ('answer',)

    def save(self, *args, **kwargs):
        inst = ModelForm.save(self, args, **kwargs)
        return inst
