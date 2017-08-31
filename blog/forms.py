from django import forms
from .models import Post
from tinymce.widgets import TinyMCE


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
            'publish': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
            'content': TinyMCE()
        }
        fields = [
            'headimage',
            'title',
            'content',
            'draft',
            'tag',
            'publish',
        ]
