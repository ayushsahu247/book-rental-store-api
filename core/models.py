from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=200, default="")
    def __str__(self):
        return self.user.username

# if I inherited the user model, then all these properties would directly be part of the AppUser
# but auth.login and auth.logout wouldnt be so simple. Right? Because that only works on the user model