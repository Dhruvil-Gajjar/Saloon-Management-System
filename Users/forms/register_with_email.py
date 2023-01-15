from django import forms
from django.contrib.auth import (
    password_validation,
)
from django.contrib.auth.forms import UserCreationForm

from Users.models import Users


class RegisterEmailForm(UserCreationForm):
    password1 = forms.CharField(
        help_text=password_validation.password_validators_help_text_html(),
        label="Password",
        widget=forms.PasswordInput(attrs={'required': True}), )
    password2 = forms.CharField(
        help_text="Enter the same password as before, for verification.",
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'required': True}), )

    class Meta:
        model = Users
        fields = ("email", "first_name", "last_name", "password1", "password2")
        widgets = {
            'first_name': forms.TextInput(attrs={'required': True}),
            'last_name': forms.TextInput(attrs={'required': True}),
            'email': forms.TextInput(attrs={'required': True})
        }
