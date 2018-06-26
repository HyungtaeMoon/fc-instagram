from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class PostForm(forms.Form):
    text = forms.CharField(max_length=50)
    file = forms.FileField()