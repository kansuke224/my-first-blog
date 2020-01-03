from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Optional.')
    password1 = forms.CharField(max_length=30, required=True, help_text='Optional.')
    password2 = forms.CharField(max_length=30, required=True, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )

     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
