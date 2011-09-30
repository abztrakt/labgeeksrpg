from django import forms
from labgeeksrpg.people.models import UserProfile, TimePeriod

class SelectTimePeriodForm(forms.Form):
    filter_choices = [['avail','Availability'],['prefs','Preferences']]
    time_periods = forms.ChoiceField(choices=[(tp.name,tp.name) for tp in TimePeriod.objects.all()])
    time_period_filter = forms.ChoiceField(required=True, label=False, widget=forms.RadioSelect(), choices=filter_choices)

