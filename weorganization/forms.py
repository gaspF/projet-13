from django import forms
from .models import *


class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ['day_name']


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['activity', 'resource', 'starting_time', 'ending_time']


class ActivityTypeForm(forms.ModelForm):
    class Meta:
        model = ActivityType
        fields = '__all__'
