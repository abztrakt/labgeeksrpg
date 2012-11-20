from django import forms
from django.forms import ModelForm
from labgeeksrpg.people.models import *
import os


class CreateUserProfileForm(ModelForm):
    def save(self, *args, **kwargs):
        inst = ModelForm.save(self, *args, **kwargs)
        return inst

    def clean_image(self):
        image = self.cleaned_data.get('staff_photo', False)
        if image:
            if image._size > 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 2mb )")
            return image


class Meta:
        model = UserProfile
        fields = ('staff_photo', 'call_me_by', 'working_periods', 'grad_date', 'office', 'about_me', 'phone', 'alt_phone')


class CreatePerformanceReviewForm(ModelForm):
    def save(self, *args, **kwargs):
        inst = ModelForm.save(self, *args, **kwargs)
        return inst

    class Meta:
        model = PerformanceReview


class CreateUWLTReviewForm(CreatePerformanceReviewForm):

    RANK_CHOICES = [(1, '1 (Unsatisfactory)')] + [(2, '2 (Needs Improvement)')] + [(3, '3 (Meets Expectations)')] + [(4, '4 (Exceeds Expectations)')] + [(5, '5 (Outstanding)')]
    HELP_TEXT_CHOICES = {
        'teamwork': 'Participates effectively in team efforts and encourages others. Treats people with fairness and respect. Carefully considers other points of view. Promotes collaboration amongst all student staff.',
        'customer_service': 'Is professional in dealing with customers and satisfies their needs within the parameters of the service we provide.',
        'dependability': 'Is responsible and punctual, has good attendance, and finds a substitute when unable to work.',
        'integrity': 'Adheres to the UW principles and standards of conduct. Actively demonstrates commitment to UW computing policies. Honors commitments, earns trust.',
        'communication': 'Expresses thoughts clearly in a way others understand and accept.',
        'initiative': 'Offers suggestions for new or better methods of operations. Looks for opportunities for self-improvement.',
        'attitude': 'Is enthusiastic, interested, diligent, and courteous.',
        'productivity': 'Takes initiative to complete tasks and achieve goals. Plans and organizes work to improve output. Completes assigned projects by agreed completion date.',
        'technical_knowledge': 'Has increased knowledge of hardware and/or software. Is up to date with the development of the UWTSC technical environment.',
        'responsibility': 'Willingness to take on responsibility.',
        'policies': 'Knows and enforces UW, C&C and staff policies.',
        'procedures': 'Understands and follows departmental procedures.',
    }

    teamwork = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text=HELP_TEXT_CHOICES['teamwork'], required=False, initial=1)
    customer_service = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text=HELP_TEXT_CHOICES['customer_service'], required=False, initial=1)
    dependability = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text=HELP_TEXT_CHOICES['dependability'], required=False, initial=1)
    integrity = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text=HELP_TEXT_CHOICES['integrity'], required=False, initial=1)
    communication = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text=HELP_TEXT_CHOICES['communication'], required=False, initial=1)
    initiative = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text=HELP_TEXT_CHOICES['initiative'], required=False, initial=1)
    attitude = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text=HELP_TEXT_CHOICES['attitude'], required=False, initial=1)
    productivity = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text=HELP_TEXT_CHOICES['productivity'], required=False, initial=1)
    technical_knowledge = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text=HELP_TEXT_CHOICES['technical_knowledge'], required=False, initial=1)
    responsibility = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text=HELP_TEXT_CHOICES['responsibility'], required=False, initial=1)
    policies = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text=HELP_TEXT_CHOICES['policies'], required=False, initial=1)
    procedures = forms.ChoiceField(widget=forms.RadioSelect, choices=RANK_CHOICES, help_text=HELP_TEXT_CHOICES['procedures'], required=False, initial=1)

    def save(self, *args, **kwargs):
        inst = ModelForm.save(self, *args, **kwargs)
        return inst

    class Meta:
        model = UWLTReview
        fields = (
            'teamwork',
            'teamwork_comments',
            'customer_service',
            'customer_service_comments',
            'dependability',
            'dependability_comments',
            'integrity',
            'integrity_comments',
            'communication',
            'communication_comments',
            'initiative',
            'initiative_comments',
            'attitude',
            'attitude_comments',
            'productivity',
            'productivity_comments',
            'technical_knowledge',
            'technical_knowledge_comments',
            'responsibility',
            'responsibility_comments',
            'policies',
            'policies_comments',
            'procedures',
            'procedures_comments',
            'comments',
        )
        exclude = ('user', 'reviewer', 'date')


class CreateFinalUWLTReviewForm(CreateUWLTReviewForm):
    WEIGHTS = UWLTReviewWeights.objects.all().order_by('effective_date').reverse()

    missed_shifts = forms.IntegerField(required=False, help_text='Enter the number of shifts the user has missed.')
    tardies = forms.IntegerField(required=False, help_text='Enter the number of shifts the user was late to.')
    is_final = forms.BooleanField(required=False, help_text='CHECK THIS ONLY WHEN THE REVIEW IS READY TO BE FINALIZED.')
    if WEIGHTS:
        weights = forms.ModelChoiceField(required=False, queryset=WEIGHTS, help_text="Choose a set of weights for this review", initial=WEIGHTS[0])
    else:
        weights = forms.ModelChoiceField(required=False, queryset=WEIGHTS, help_text="No weights for reviews created yet")

    def __init__(self, *args, **kwargs):
        super(CreateUWLTReviewForm, self).__init__(*args, **kwargs)

    class Meta(CreateUWLTReviewForm.Meta):
        fields = (
            'teamwork',
            'teamwork_comments',
            'customer_service',
            'customer_service_comments',
            'dependability',
            'dependability_comments',
            'integrity',
            'integrity_comments',
            'communication',
            'communication_comments',
            'initiative',
            'initiative_comments',
            'attitude',
            'attitude_comments',
            'productivity',
            'productivity_comments',
            'technical_knowledge',
            'technical_knowledge_comments',
            'responsibility',
            'responsibility_comments',
            'policies',
            'policies_comments',
            'procedures',
            'procedures_comments',
            'comments',
            'missed_shifts',
            'missed_shifts_comments',
            'tardies',
            'tardies_comments',
            'weights',
            'is_final',
        )


class UpdateWageHistoryForm(ModelForm):

    WH_REASONS = WageChangeReason.objects.all()
    if not WH_REASONS:
        default = WageChangeReason.objects.create(title='Starting Wage')
        WH_REASONS = WageChangeReason.objects.all()

    wage_change_reason = forms.ModelChoiceField(required=True, queryset=WH_REASONS, help_text="Choose a reason for this wage change (not recorded if no wage change)", initial=WH_REASONS[0])

    def __init__(self, *args, **kwargs):
        # successfully passes user to the form
        user = kwargs.pop('user')
        LATEST_WH = WageHistory.objects.filter(user=user).order_by('effective_date').reverse()
        super(UpdateWageHistoryForm, self).__init__(*args, **kwargs)
        # python uses the following correctly, but help_text doesn't make it to the view for some reason.
        if LATEST_WH:
            wage = forms.FloatField(required=True, help_text="Enter the updated wage for this user", initial=LATEST_WH[0].wage)
        else:
            wage = forms.FloatField(required=True, help_text="Enter the wage for this user")

    def save(self, *args, **kwargs):
        inst = ModelForm.save(self, *args, **kwargs)
        return inst

    class Meta:
        model = WageHistory
        fields = (
            'wage',
            'wage_change_reason',
        )
