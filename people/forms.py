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

    RANK_CHOICES = [(0,'N/A')] + [(i,i) for i in range (1,6)]
    HELP_TEXT_CHOICES = {
        'teamwork': 'Participates effectively in team efforts and encourages others. Treats people with fairness and respect. Carefully considers other points of view. Promotes collaboration amongst all student staff.',
        'customer_service': 'Is professional in dealing with customers and satisfies their needs within the parameters of the service we provide.',
        'dependability': 'Is responsible and punctual, has good attendance, and finds a substitute when unable to work.',
        'integrity': 'Adheres to the UW principles and standards of conduct. Actively demonstrates commitment to UW computing policies. Honors commitments, earns trust.',
        'communication':'Expresses thoughts clearly in a way others understand and accept.',
        'initiative': 'Offers suggestions for new or better methods of operations. Looks for opertunities for self improvment.',
        'attitude': 'Is enthusiastic, interested, dilligent, and courteous.',
        'productivity':'Takes initiative to complete tasks and achieve goals. Plans and organizes work to improve output. Completes assigned projects by agreed completion date.',
        'technical_knowledge': 'Has increased knowledge of hardware and/or software. Is up to date with the development of the UWTSC technical environment.',
        'responsibility': 'Willingness to take on responsibility.',
        'policies':'Knows and enforces UW, C&C and staff policies.',
        'procedures':'Understands and follows departamental procedures.',
    }

    teamwork = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text = HELP_TEXT_CHOICES['teamwork']) 
    customer_service = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text = HELP_TEXT_CHOICES['customer_service'])
    dependability = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text = HELP_TEXT_CHOICES['dependability'])
    integrity = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text = HELP_TEXT_CHOICES['integrity'])
    communication = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text = HELP_TEXT_CHOICES['communication'])
    initiative = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text = HELP_TEXT_CHOICES['initiative'])
    attitude = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text = HELP_TEXT_CHOICES['attitude'])
    productivity = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text = HELP_TEXT_CHOICES['productivity'])
    technical_knowledge = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text = HELP_TEXT_CHOICES['technical_knowledge'])
    responsibility = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES,help_text = HELP_TEXT_CHOICES['responsibility'])
    policies = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES,help_text = HELP_TEXT_CHOICES['policies'])
    procedures = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES,help_text = HELP_TEXT_CHOICES['procedures'])

    def save(self,*args,**kwargs):
        inst = ModelForm.save(self, *args, **kwargs)
        return inst

    class Meta:
        model = UWLTReview
        fields = (
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
        )
        exclude = ('user','reviewer','date')

class CreateFinalUWLTReviewForm(CreateUWLTReviewForm):

    missed_shifts = forms.IntegerField()
    tardies = forms.IntegerField()
    is_final = forms.BooleanField()
    def __init__(self,*args,**kwargs):
        super(CreateUWLTReviewForm,self).__init__(*args,**kwargs)
        
