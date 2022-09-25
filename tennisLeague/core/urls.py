from core import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('rules', views.rules, name='rules'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),  
    path('logout', views.logout_view, name='logout'),
]
