from django.contrib import admin
from django.urls import path
from .views import *
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('createweekly', login_required(CreateWeekly.as_view()), name='create-weekly-sheet'),
    path('existingsheet', login_required(ExistingSheet.as_view()), name='existing-sheet'),
    path('existingsheet/<int:pk>/delete', views.DeleteActivity.as_view(), name='activity-delete'),

]

