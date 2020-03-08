from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', Index.as_view(), name='apprendre13-index'),
    path('createprofile/', login_required(CreateProfile.as_view()), name='create-profile'),
    path('profilelist/', login_required(ProfileList.as_view()), name='profile-list'),
    path('profilesheet/<int:id>', login_required(ProfileSheet.as_view()), name='profile-sheet'),
    path('profilelist/<int:pk>/delete', views.DeleteProfile.as_view(), name='profile-delete'),

]
