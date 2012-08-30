from django import forms
from labgeeksrpg.chronos.models import Shift


class ShiftForm(forms.ModelForm):
    """ The form that submits a sign in / sign out of a shift.
    """
    class Meta:
        model = Shift
        exclude = ('person', 'intime', 'outtime', 'in_clock', 'out_clock')
