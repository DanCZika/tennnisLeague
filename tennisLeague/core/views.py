from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import PlayerData

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

# @login_required

def profile(request):

    args = {'user' : request.user}
    return render(request, 'profile.html', args)