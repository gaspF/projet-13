from django import forms
from .models import Post
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.helper import FormHelper


class PostForm(forms.ModelForm):
    """Post form"""
    class Meta:
        model = Post
        fields = ('Sujet', 'Texte',)
