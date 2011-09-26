from django import forms
from django.forms import ModelForm
from labgeeksrpg.people.models import UserProfile
import os

class CreateUserProfileForm(ModelForm):

    def get_css_files():
        css_choices = []
        path = 'static/'
        for infile in os.listdir(path):
                if infile.endswith(".css"):
                    css_choices.append((infile,infile))
        return css_choices
        
    site_skin = forms.ChoiceField(choices=get_css_files())

    def save(self,*args,**kwargs):
        inst = ModelForm.save(self, *args,**kwargs)
        return inst
    class Meta:
        model = UserProfile
        fields = ('staff_photo','call_me_by','working_periods', 'grad_date','office','about_me','phone','alt_phone','site_skin')
