# apis/forms.py

from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'phone_number', 'gmail', 'login_password', 'app_password']
