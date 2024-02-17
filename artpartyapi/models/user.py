from django.db import models


class User(models.Model):

    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    img = models.CharField(max_length=500)
    uid = models.CharField(max_length=50)
