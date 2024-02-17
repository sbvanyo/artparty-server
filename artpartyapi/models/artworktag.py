from django.db import models
from .artwork import Artwork
from .tag import Tag


class ArtworkTag(models.Model):

    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
