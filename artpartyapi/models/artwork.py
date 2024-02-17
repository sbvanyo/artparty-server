from django.db import models
from .user import User
from .artist import Artist


class Artwork(models.Model):

    title = models.CharField(max_length=50)
    img = models.CharField(max_length=500)
    medium = models.CharField(max_length=500)
    description = models.TextField()
    date = models.DateField()
    age = models.IntegerField()
    featured = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
