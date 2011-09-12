from django import forms
from django.forms import ModelForm
from labgeeksrpg.people.models import UserProfile

class CreateUserProfileForm(ModelForm):

    def save(self,*args,**kwargs):
        inst = ModelForm.save(self, *args,**kwargs)
        return inst
    class Meta:
        model = UserProfile
        fields = ('staff_photo','call_me_by','grad_date','office','about_me','phone','alt_phone')
