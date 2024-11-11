from django.forms import ModelForm
from .models import Job

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Editted Registration
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = '__all__'