from django import forms
from labgeeksrpg.chronos.models import Shift

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
