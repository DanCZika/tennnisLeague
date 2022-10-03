from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import PlayerData

class EditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )

class EditPhoneNumber(forms.Form):
    phone_number = forms.CharField(label='Your new phone number:', max_length=100)  