from django import forms


class UploadFileForm(forms.Form):
    xlxs = forms.FileField()
    imgzipped = forms.FileField()
