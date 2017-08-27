from django import forms
from .models import PresRec


class PresForm(forms.ModelForm):
    class Meta:
        model = PresRec
        fields = [
            'student',
            'is_absent',
            'date',
            'subject',
        ]
