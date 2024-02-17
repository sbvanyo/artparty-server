from django.db import models
from .user import User


class Artist(models.Model):

    name = models.CharField(max_length=50)
    img = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
