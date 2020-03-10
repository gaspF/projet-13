from django import forms
from .models import *


class DayForm(forms.ModelForm):
    """Day form, enumerate type"""
    class Meta:
        model = Day
        fields = ['day_name']


class ActivityForm(forms.ModelForm):
    """Activity form"""
    class Meta:
        model = Activity
        fields = ['activity', 'resource', 'starting_time', 'ending_time']


class ActivityTypeForm(forms.ModelForm):
    """Activity type form, enumerate type"""
    class Meta:
        model = ActivityType
        fields = '__all__'
