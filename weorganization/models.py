from django.db import models
from django_enumfield import enum
from django.utils.translation import ugettext_lazy
from website.models import Profile
from datetime import datetime, timedelta
from django.contrib.auth.models import User



class ActivityTypeList(enum.Enum):
    """Enumerate data model of activlty types"""
    PRATIQUED = 1
    SEANCEG = 2
    ACTIVITECOMP = 3
    FREETIME = 4
    ELSE = 5

    __labels__ = {
        PRATIQUED: ugettext_lazy('Pratique délibérée'),
        SEANCEG: ugettext_lazy('Séance guidée'),
        ACTIVITECOMP: ugettext_lazy('Activité complémentaire'),
        FREETIME: ugettext_lazy('Temps libre'),
        ELSE: ugettext_lazy('Autre'),
    }


class ActivityType(models.Model):
    type_activity = enum.EnumField(ActivityTypeList)


class DayList(enum.Enum):
    """Enumerate data model of days"""
    LUNDI = 1
    MARDI = 2
    MERCREDI = 3
    JEUDI = 4
    VENDREDI = 5
    SAMEDI = 6
    DIMANCHE = 7

    __labels__ = {
        LUNDI: ugettext_lazy('Lundi'),
        MARDI: ugettext_lazy('Mardi'),
        MERCREDI: ugettext_lazy('Mercredi'),
        JEUDI: ugettext_lazy('Jeudi'),
        VENDREDI: ugettext_lazy('Vendredi'),
        SAMEDI: ugettext_lazy('Samedi'),
        DIMANCHE: ugettext_lazy('Dimanche')
    }


class Activity(models.Model):
    """Activity main class, which contains activity name, resource type, activity type, starting and ending time"""
    activity = models.CharField(verbose_name='Activité', max_length=200)
    resource = models.CharField(verbose_name='Ressource', max_length=200)
    type = models.ForeignKey(ActivityType, verbose_name='type', on_delete=models.CASCADE)
    starting_time = models.TimeField(verbose_name="Heure de début", auto_now=False, auto_now_add=False, default=datetime.now().replace(second=0, microsecond=0))
    ending_time = models.TimeField(verbose_name="Heure de fin", auto_now=False, auto_now_add=False, default=datetime.now().replace(hour=22, minute=22, second=0, microsecond=0))


class Day(models.Model):
    """Day class, which is linked to an activity, in order to display what activities is scheluled on which day."""
    day_name = enum.EnumField(DayList)
    daily_activity = models.ForeignKey(Activity, verbose_name='Activité liée', default="99999", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, verbose_name='Profil lié', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Utilisateur lié', on_delete=models.CASCADE)
