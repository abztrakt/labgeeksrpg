from django import forms
from django.forms import ModelForm
from labgeeksrpg.sybil.models import *


class UploadPictureForm(ModelForm):

    def save(self, *args, **kwargs):
        instance = ModelForm.save(self, *args, **kwargs)
        return instance

    class Meta:
        model = Screenshot
        fields = ('picture',)
