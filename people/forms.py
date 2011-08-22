from django import forms
from django.forms import ModelForm
from labgeeksrpg.people.models import UserProfile

class CreateUserProfileForm(ModelForm):

    def save(self,*args,**kwargs):
        inst = ModelForm.save(self, *args,**kwargs)
        return inst
    class Meta:
        model = UserProfile
        fields = ('user','staff_photo','call_me_by','status','start_date','end_date','grad_date','supervisor','title','office','working_periods','about_me','phone','alt_phone')

