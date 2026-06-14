from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True, help_text="Required. Enter your full name.")

    class Meta:
        model = User
        fields = ("name", "email", "username", "password1", "password2")

