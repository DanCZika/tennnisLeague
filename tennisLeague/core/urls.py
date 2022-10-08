from core import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('rules', views.rules, name='rules'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('success', views.success, name='success'),
    path('profile', views.view_profile, name='view_profile'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('profile/editphonenumber', views.edit_phonenumber, name='edit_phonenumber'),
    path('enroll', views.enter_round, name='enter_round'),
    path('enrolled', views.enrolled, name='enrolled'),
    path('unenrolled', views.unenrolled, name='unenrolled'),
    path('score', views.show_score, name='show_score'),
]
