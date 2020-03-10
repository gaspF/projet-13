from django.db import models
from django.contrib.auth.models import User
import datetime


class Profile(models.Model):
    name = models.CharField(verbose_name="Nom du projet", max_length=500)
    objective = models.TextField(verbose_name="Objectif stratégique", max_length=4000)
    starting_date = models.DateField(verbose_name="Date de commencement", default=datetime.date.today)
    ending_date = models.DateField(verbose_name="Date de fin", default=datetime.date.today)
    hourly_volume = models.SmallIntegerField(verbose_name="Volume horaire total à consacrer par semaine")
    forces = models.TextField(verbose_name="Forces", max_length=8000)
    weaknesses = models.TextField(verbose_name="Faiblesses", max_length=8000)
    opportunities = models.TextField(verbose_name="Opportunités", max_length=8000)
    menaces = models.TextField(verbose_name="Menaces", max_length=8000)
    offensive = models.TextField(verbose_name="Offensive", max_length=8000)
    defensive = models.TextField(verbose_name="Défensive", max_length=8000)
    preventive = models.TextField(verbose_name="Préventive", max_length=8000)
    emergency = models.TextField(verbose_name="Urgence", max_length=8000)
    step_1 = models.CharField(verbose_name="Activité 1", max_length=2000)
    step_1_duration = models.SmallIntegerField(verbose_name="Volume horaire par semaine", default=1)
    step_2 = models.CharField(verbose_name="Activité 2", max_length=2000)
    step_2_duration = models.SmallIntegerField(verbose_name="Volume horaire par semaine", default=1)
    step_3 = models.CharField(verbose_name="Activité 3", max_length=2000)
    step_3_duration = models.SmallIntegerField(verbose_name="Volume horaire par semaine", default=1)
    step_4 = models.CharField(verbose_name="Activité 4", max_length=2000, blank=True)
    step_4_duration = models.SmallIntegerField(verbose_name="Volume horaire par semaine", default=1)
    step_5 = models.CharField(verbose_name="Activité 5", max_length=2000, blank=True)
    step_5_duration = models.SmallIntegerField(verbose_name="Volume horaire par semaine", default=1)
    step_6 = models.CharField(verbose_name="Activité 6", max_length=2000, blank=True)
    step_6_duration = models.SmallIntegerField(verbose_name="Volume horaire par semaine", default=1)

    def __str__(self):
        return self.name


class SavedProfile(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['saved_by', 'saved_profile'], name='saved_association'),
        ]
    saved_by = models.ForeignKey(User, verbose_name='Sauvegardé par', on_delete=models.CASCADE,)
    saved_profile = models.ForeignKey(Profile, verbose_name="Profil sauvegardé", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
