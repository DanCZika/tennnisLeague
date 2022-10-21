from tokenize import group
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import PlayerData, Match


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

class SubmitMatchScoreForm(forms.Form):
    # start_date = forms.DateField(label='Date of the match:')
    court = forms.CharField(label='The court the match was played on:', max_length=100)
    score = forms.CharField(label='Score:', max_length=100)



class ReportScoreForm(forms.Form):
    player2 = forms.CharField(
        required=True , max_length=255, label='Your opponent name:',
        widget=forms.TextInput(attrs={'placeholder': 'J. Doe'}),
        )
    court = forms.CharField(required=True , label='Court:', max_length=100)
    #ROUND_NAMES = [('Round 1 - Group A', 'Group A'), ('Round 1 - Group B', 'Group B')]
    ROUND_NAMES = [('Round 1', 'Group A'), ('Demo Round', 'Group B')]
    round = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.Select(choices=ROUND_NAMES),
    )

    score = forms.CharField(
        label='Score:',
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': '6:0 , 6:0'}),
        help_text= 'Format: 7:6 , 3-6 , 10:4'
        )
