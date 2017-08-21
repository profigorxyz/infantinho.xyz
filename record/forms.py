from django import forms
from .models import PresRec


class PresForm(forms.ModelForm):
    class Meta:
        model = PresRec
