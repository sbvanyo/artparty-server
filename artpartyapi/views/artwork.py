"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from artpartyapi.models import Artwork


class ArtworkView(ViewSet):
    """Artwork view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single artwork
        Returns: Response -- JSON serialized artwork"""
        artwork = Artwork.objects.get(pk=pk)
        serializer = ArtworkSerializer(artwork)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all artworks
        Returns: Response -- JSON serialized list of artworks"""
        artworks = Artwork.objects.all()
        serializer = ArtworkSerializer(artworks, many=True)
        return Response(serializer.data)


class ArtworkSerializer(serializers.ModelSerializer):
    """JSON serializer for artworks"""
    class Meta:
        model = Artwork
        fields = ('id', 'user', 'artist', 'title', 'img', 'medium', 'description', 'date', 'age', 'featured')
        depth = 1
