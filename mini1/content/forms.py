from django.contrib.auth.forms import UserChangeForm
from user.models import User
from django.contrib.auth import get_user_model
from django import forms

class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = get_user_model()
        fields = ['age', 'nickname',]



