from bdb import set_trace
import bdb
import pdb
from readline import insert_text
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import PlayerData, Entry, Round
from .forms import EditProfileForm, EditPhoneNumber, RegistrationForm
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
            return redirect('success') #change it to login once implemented

    else:
        form = UserCreationForm()
    context = {
        'form':form
    }
    return render(request, 'register.html', context)

def reg_form(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        set_trace()
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = RegistrationForm()

    args = {'form': form}

    return render(request, 'reg_form.html', args)

def success(request):
    return render(request, 'success.html')

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

@login_required
def enter_round(request):
    user  = request.user
    playerdata = user.playerdata
    #if they havent submitted personal info redirect to page
    #should be revritten to be more clear
    profileOK = 1
    if user.first_name == '' or user.last_name == '' or user.email == '' or playerdata.phone_number == '':
        profileOK = 0
    #code to run if profile is complete
    #check if enrolled
    enrolled = 0

    if len(Entry.objects.filter(player = request.user.pk)) != 0:
        enrolled = 1
    else:
        # pdb.set_trace()
        enrolled = 0

    if request.method == 'POST' and enrolled == 0:
        #create Entry
        enrollment = Entry(player = request.user)
        enrollment.save()
        return redirect('enrolled')


    elif request.method == 'POST' and enrolled == 1:
        Entry.objects.filter(player = request.user.pk).delete()
        return redirect('unenrolled')

    return render(request, 'enroll.html', {'enrolled' : enrolled, 'profileOK' : profileOK})

def enrolled(request):
    return render(request, 'enrolled.html')

def unenrolled(request):
    return render(request, 'unenrolled.html')

def show_score(request):
    playerno = len(Entry.objects.all())
    return render(request, 'show_score.html', {'player_no' : playerno})

def show_score_active(request):
    ### The view to show after the round started###
    #First log the entries and pass them into the return arg
    CURRENT_ROUND = 'Round 1'
    round = Round.objects.get(name = CURRENT_ROUND)
    #filter and order the by score
    players = Entry.objects.filter(round = round).order_by('-score')
    # pdb.set_trace()
    args = {'players' : players }
    playerno = len(Entry.objects.all())
    return render(request, 'show_score_active.html', args)