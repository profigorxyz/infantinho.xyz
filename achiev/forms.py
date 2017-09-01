from django import forms


class UploadAchiev(forms.Form):
    xlxs = forms.FileField()
