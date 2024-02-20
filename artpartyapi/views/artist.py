"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from artpartyapi.models import Artist, User


class ArtistView(ViewSet):
    """Artist view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single artist
        Returns: Response -- JSON serialized artist"""
        try:
            artist = Artist.objects.get(pk=pk)
            serializer = ArtistSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all artists
        Returns: Response -- JSON serialized list of artists"""
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)
    
    
    def create(self, request):
        """Handle POST operations
        Returns Response -- JSON serialized artist instance"""
        user = User.objects.get(pk=request.data["user"])

        artist = Artist.objects.create(
            name=request.data["name"],
            img=request.data["img"],
            user=user,
        )
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def update(self, request, pk):
        """Handle PUT requests for an artist
        Returns: Response -- Empty body with 204 status code"""

        artist = Artist.objects.get(pk=pk)
        artist.name = request.data["name"]
        artist.img = request.data["img"]

        user = User.objects.get(pk=request.data["user"])
        artist.user = user
        artist.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)



class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists"""
    class Meta:
        model = Artist
        fields = ('id', 'user', 'name', 'img')
        # depth = 1
