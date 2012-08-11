from labgeeksrpg.knowledgebase.models import Issue, Resolution
from django import forms
from django.forms import ModelForm


class CreateIssueForm(ModelForm):
    """
    Handles the creation of issues that need solving
    """
    # TODO: after importing TinyMCE to path use tinyMCE widget
    content = forms.CharField(widget=forms.Textarea, help_text='Describe your issue in detail', required=True)

    class Meta:
        model = Issue
        fields = ('content',)

    def save(self, *args, **kwargs):
        inst = ModelForm.save(self, *args, **kwargs)
        return inst
