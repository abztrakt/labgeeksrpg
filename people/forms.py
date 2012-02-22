from django import forms
from django.forms import ModelForm
from labgeeksrpg.people.models import *
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


class CreatePerformanceReviewForm(ModelForm):
    def save(self,*args,**kwargs):
        inst = ModelForm.save(self,*args,**kwargs)
        return inst

    class Meta:
        model = PerformanceReview
        
class CreateUWLTReviewForm(CreatePerformanceReviewForm):

    RANK_CHOICES = [(i,i) for i in range (0,6)]

    teamwork = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES)
    customer_service = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES)
    dependability = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES)
    integrity = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES)
    communication = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES)
    initiative = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES)
    attitude = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES)
    productivity = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES)
    technical_knowledge = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES)
    responsibility = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES)
    policies = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES)
    procedures = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES)
    #missed_shifts = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES)
    #tardies = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES)

    def save(self,*args,**kwargs):
        inst = ModelForm.save(self, *args, **kwargs)
        return inst

    class Meta:
        model = UWLTReview
        fields = (
            'date',
            'teamwork',
            'customer_service',
            'dependability', 
            'integrity', 
            'communication',
            'initiative', 
            'attitude', 
            'productivity', 
            'technical_knowledge', 
            'responsibility',
            'policies',
            'procedures', 
            'comments',
            'is_final',
        )
        exclude = ('user','reviewer',)
