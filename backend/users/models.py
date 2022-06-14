from django.contrib.auth.models import User
from django.db import models


class Tier(models.Model):
   name = models.CharField(max_length=100, default="Basic")
   thumbnail_sizes = models.CharField(max_length=200, default="200")
   link_to_original = models.IntegerField(default=0)
   expiring = models.CharField(max_length=20, default="0")

   def __str__(self):
        return f'{self.name} Tier'


class UserProfile(models.Model):
   user = models.OneToOneField(
      User, on_delete=models.CASCADE, related_name="profile")
   tier = models.ForeignKey(
      Tier, on_delete=models.SET_DEFAULT,
      default=1, related_name="tier")

   def __str__(self):
        return f'{self.user.username}'

