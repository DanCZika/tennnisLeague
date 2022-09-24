from django.shortcuts import render

# Create your views here.
def index(request):
    my_dict = {'insert_me': "inserted text"}
    return render(request, 'index.html', my_dict)

def rules(request):
    # my_dict = {'insert_me': "ide tette"}
    return render(request, 'rules.html')