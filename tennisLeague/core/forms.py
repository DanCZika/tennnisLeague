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
        )

class EditPhoneNumber(forms.Form):

    class Meta:
        model = PlayerData
        fields = ('phone_number',)