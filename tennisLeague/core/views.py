from bdb import set_trace
import bdb
import pdb
from readline import insert_text
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import PlayerData
from .forms import EditProfileForm, EditPhoneNumber
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    my_dict = {'insert_me': "inserted text"}
    return render(request, 'index.html', my_dict)

def rules(request):
    # my_dict = {'insert_me': "ide tette"}
    return render(request, 'rules.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()          
            messages.info(request, 'Your registration was successful!')
            return redirect('index') #change it to login once implemented

    else:
        form = UserCreationForm()
    context = {
        'form':form
    }
    return render(request, 'register.html', context)

def login_view(request):
    # return render(request, 'register.html')
    if request.method == 'POST':
        print("got the post")
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            #Check if the corresponding Playerdata exists, if not create
            try:
                playerdata = PlayerData.objects.get(pk = request.user.pk)
            except ObjectDoesNotExist:
                # pdb.set_trace()
                playerdata = PlayerData(pk = request.user.pk )
                playerdata.save()


            return redirect('index')
    else:
        form = AuthenticationForm()
    context = {
        'form':form
    }
    return render(request, 'login.html', context)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        print("logging out")
        return redirect('index')

@login_required
def view_profile(request):
    user  = request.user
    playerdata = user.playerdata
    # pdb.set_trace()
    args = {'user' : user, 'playerdata' : playerdata}
    return render(request, 'profile.html', args)

@login_required
def edit_profile(request):
    user  = request.user
    playerdata = user.playerdata
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance = user)
        if form.is_valid:
            form.save()
            return redirect('view_profile')

    else:
        form = EditProfileForm(instance = user)
        args = {'form' : form}
        return render(request, 'edit_profile.html', args)

@login_required
def edit_phonenumber(request):
    user  = request.user
    playerdata = user.playerdata
    if request.method == 'POST':
        form = EditPhoneNumber(request.POST)
        if form.is_valid():
            playerdata.phone_number = form.cleaned_data['phone_number']
            playerdata.save()
            return redirect('view_profile')

    else:
        form = EditPhoneNumber()
        args = {'form' : form}
        return render(request, 'edit_profile.html', args)