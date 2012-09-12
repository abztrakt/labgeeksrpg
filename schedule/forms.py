from django import forms
from labgeeksrpg.people.models import UserProfile
from labgeeksrpg.schedule.models import TimePeriod
from labgeeksrpg.chronos.models import Location

class SelectTimePeriodForm(forms.ModelForm):

    working_periods = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        queryset=TimePeriod.objects.all().order_by('start_date'),
        help_text='Please select the time periods in which you are available for work.' 
    )

    def save(self,*args,**kwargs):
        inst = forms.ModelForm.save(self,*args,**kwargs)
        return inst

    class Meta:
        model = UserProfile
        fields = ('working_periods',)

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
    location = forms.ChoiceField(choices=[(loc.name,loc.name) for loc in Location.objects.all()],required=True)


class SelectDailyScheduleForm(forms.Form):
    location = forms.ChoiceField(widget=forms.RadioSelect,choices=[(loc.name,loc.name) for loc in Location.objects.all()],required=True)
    day = forms.DateField()
