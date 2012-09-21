from django import forms
from django.forms import ModelForm
from labgeeksrpg.sybil.models import *


class UploadPictureForm(ModelForm):

    def save(self, *args, **kwargs):
        instance = ModelForm.save(self, *args, **kwargs)
        return instance

    def clean_image(self):
        image = self.cleaned_data.get('picture', False)
        if image:
            if image._size > 1920 * 1080:  # 1080p max realistic screenshot (2MP ~ 2MB)
                raise forms.ValidationError("Image file too large")
            return image

    class Meta:
        model = Screenshot
        fields = ('picture',)


class CreateTagForm(ModelForm):

    class Meta:
        model = Tag
        fields = ('name', 'description',)

    def save(self, *args, **kwargs):
        instance = ModelForm.save(self, *args, **kwargs)
        return instance
