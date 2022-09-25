from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

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

