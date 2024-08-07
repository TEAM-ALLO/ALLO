from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'profile_image']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
