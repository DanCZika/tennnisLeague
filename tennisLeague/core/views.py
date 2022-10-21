from bdb import set_trace
from os import uname
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
from .models import Match, PlayerData, Entry, Round, MatchEntry
from .forms import EditProfileForm, EditPhoneNumber, RegistrationForm,SubmitMatchScoreForm
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
    CURRENT_ROUND_A = 'Round 1'
    CURRENT_ROUND_B = 'Demo Round'
    round_a = Round.objects.get(name = CURRENT_ROUND_A)
    round_b = Round.objects.get(name = CURRENT_ROUND_B)
    #filter and order the by score
    players_a = Entry.objects.filter(round = round_a).order_by('-score')
    players_b = Entry.objects.filter( round = round_b).order_by('-score')
    # pdb.set_trace()
    #filter matches
    matches_a = Match.objects.filter(round = round_a , played = True).order_by('start_date')
    matches_b = Match.objects.filter(round = round_b , played = True).order_by('start_date')

    args = {'players_a' : players_a, 'matches_a' :  matches_a, 'players_b' : players_b, 'matches_b' :  matches_b}
    playerno = len(Entry.objects.all())
    return render(request, 'show_score_active.html', args)

@login_required
def match_list(request):
    ### make query with all the
    #query user
    user  = request.user
    entry = Entry.objects.filter(player = user)[0]
    #query MatchEntry
    match_entry = MatchEntry.objects.filter(player = entry)
    #don't use this queriset in live
    match_fk = []
    if len(match_entry) != 1 or len(match_entry) != 0:
        for me in match_entry:
            match_fk.append(me.match_id)

    if len(match_entry) == 1:   
        match_fk.append(match_entry[0].id)

    match = Match.objects.filter(pk__in = match_fk).filter(played = False)
    # pdb.set_trace()
    return render(request, 'match_list.html', {'matches' : match}) 

from django.shortcuts import get_object_or_404
import datetime

@login_required
def edit_score(request, pk):
    #match = Match.objects.get(pk = pk)
    match = get_object_or_404(Match, pk = pk)
    if request.method == 'POST':
        form = SubmitMatchScoreForm(request.POST)
        if form.is_valid():
            match.score = form.cleaned_data['score']
            match.court = form.cleaned_data['court']
            match.start_date = datetime.datetime.now()
            match.played = True
            match.save()
            return redirect('show_score')

    else:
        form = SubmitMatchScoreForm()
    
    args = {'form' : form, 'match' : match } 
    return render(request, 'edit_score.html', args)

from .forms import ReportScoreForm

@login_required
def report_score(request):
    user  = request.user
    u_name = str(user.first_name)[0] + '. '+ str(user.last_name)
    
    if request.method == 'POST':
        form = ReportScoreForm(request.POST)
        if form.is_valid():
            player1 = u_name
            player2 = form.cleaned_data['player2']
            court = form.cleaned_data['court']
            round_name = form.cleaned_data['round']
            round = get_object_or_404(Round, name = round_name) #Round.objects.get(name = round_name)
            score = form.cleaned_data['score']
            start_date = datetime.datetime.now()
            played = True
            match = Match(
                player1 = player1,
                player2 = player2,
                court = court,
                score = score,
                start_date = start_date,
                played = played,
                round = round,
                )
            match.save()

            return redirect('show_score')

    else:
        form = ReportScoreForm()
    # pdb.set_trace()
    args = {'form' : form, 'u_name' : u_name}
    return render(request, 'report_score.html', args)



from django.views.generic import View, ListView, TemplateView,DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class MatchListView(LoginRequiredMixin, ListView):
    model = Match