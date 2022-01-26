from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import fields
from user.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname','age']





