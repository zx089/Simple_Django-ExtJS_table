from django import forms
from django.contrib.auth.forms import AuthenticationForm


# Not needed for now
class BootstrapAuthForm(AuthenticationForm):
    username = forms.CharField(max_length=255, widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': 'User name'
    }))
    password = forms.CharField(widget=forms.PasswordInput({
        'class': 'form_control',
        'placeholder': 'Password'
    }))