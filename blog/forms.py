from django import forms
from .models import Post
from tinymce.widgets import TinyMCE


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
            'content': TinyMCE()
        }
        fields = [
            'headimage',
            'title',
            'tag',
            'content',
            'draft',
            'publish',
        ]
