from tabnanny import verbose
from django.db import models
from core.models import AppUser

# Create your models here.

class Genre(models.Model):
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.genre
    class Meta:
        verbose_name_plural  = "genre"

class Book(models.Model):
    name = models.TextField()
    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    def __str__(self):
        return self.name + " - " + self.app_user.user.username