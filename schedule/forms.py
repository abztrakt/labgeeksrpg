from django import forms
from labgeeksrpg.schedule.models import TimePeriod
from labgeeksrpg.people.models import UserProfile
from labgeeksrpg.chronos.models import Location

class SelectTimePeriodForm(forms.Form):
    filter_choices = [['avail','Availability'],['prefs','Preferences']]
    time_periods = forms.ChoiceField(choices=[(tp.name,tp.name) for tp in TimePeriod.objects.all()])
    time_period_filter = forms.ChoiceField(required=True, label=False, widget=forms.RadioSelect(), choices=filter_choices)

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

    day = forms.ChoiceField(choices=DAY_CHOICES)


class SelectDailyScheduleForm(forms.Form):
    location = forms.ChoiceField(widget=forms.RadioSelect,choices=[(loc.name,loc.name) for loc in Location.objects.all()],required=True)
    day = forms.DateField()
