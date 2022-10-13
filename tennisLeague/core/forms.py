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


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True , max_length=100)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        phone_number = self.cleaned_data['phone_number']

        if commit:
            user.save()
            playerdata = PlayerData(pk = user.pk )
            playerdata.phone_number = self.cleaned_data['phone_number']
            playerdata.save()

        return user