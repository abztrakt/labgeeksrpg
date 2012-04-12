from django import forms
from labgeeksrpg.people.models import UserProfile, TimePeriod
from labgeeksrpg.chronos.models import Location

class SelectTimePeriodForm(forms.ModelForm):
    time_periods = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[(tp.name,tp.name) for tp in TimePeriod.objects.all()])

    class Meta:
        model = UserProfile
        fields = ('time_periods',)

class CreateDailyScheduleForm(forms.Form):
    DAY_CHOICES = (
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )
    timeperiods = forms.ChoiceField(choices=[(tp.name,tp.name) for tp in TimePeriod.objects.all()])
    location = forms.ChoiceField(widget=forms.RadioSelect,choices=[(loc.name,loc.name) for loc in Location.objects.all()],required=True)


class SelectDailyScheduleForm(forms.Form):
    location = forms.ChoiceField(widget=forms.RadioSelect,choices=[(loc.name,loc.name) for loc in Location.objects.all()],required=True)
    day = forms.DateField()
