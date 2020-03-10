from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from website.models import Profile


class Post(models.Model):
    """A class that allows program to add post into database"""
    author = models.ForeignKey(User, verbose_name="Auteur", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, verbose_name="Profil lié", default="99999", on_delete=models.CASCADE)
    Sujet = models.CharField(max_length=200)
    Texte = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        """Set a publish date and hour for a new post"""
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
