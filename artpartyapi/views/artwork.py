"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from artpartyapi.models import Artwork, Artist, User, Tag, ArtworkTag
from .artworktag import ArtworkTagSerializer


class ArtworkView(ViewSet):
    """Artwork view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single artwork
        Returns: Response -- JSON serialized artwork"""
        try:
            artwork = Artwork.objects.get(pk=pk)
            serializer = ArtworkSerializer(artwork)
            return Response(serializer.data)
        except Artwork.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all artworks
        Returns: Response -- JSON serialized list of artworks"""
        artworks = Artwork.objects.all()
        serializer = ArtworkSerializer(artworks, many=True)
        return Response(serializer.data)
      
      
    def create(self, request):
        """Handle POST operations
        Returns Response -- JSON serialized artwork instance"""
        user = User.objects.get(pk=request.data["user"])
        artist = Artist.objects.get(pk=request.data["artist"])

        artwork = Artwork.objects.create(
            title=request.data["title"],
            img=request.data["img"],
            medium=request.data["medium"],
            description=request.data["description"],
            date=request.data["date"],
            age=request.data["age"],
            featured=request.data.get("featured", False),
            user=user,
            artist=artist,
        )
        
        # Handling artwork tags
        tags = request.data.get("tags", [])
        for tag_id in tags:
            try:
                tag = Tag.objects.get(id=tag_id)
                ArtworkTag.objects.create(artwork=artwork, tag=tag)
            except Tag.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ArtworkSerializer(artwork, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArtworkSerializer(serializers.ModelSerializer):
    """JSON serializer for artworks"""
    # Value of 'tags' will be computed by 'get_tags' method below
    tags = serializers.SerializerMethodField()
    class Meta:
        model = Artwork
        fields = ('id', 'user', 'artist', 'title', 'img', 'medium', 'description', 'date', 'age', 'featured', 'tags')
        # depth = 1
        
    # Serializes artwork tags
    def get_tags(self, artwork):
        """method for getting all tags"""
        # 'tags' coming from related_name='tags' in ArtworkTag model
        artworktags = artwork.tags.all()
        return ArtworkTagSerializer(artworktags, many=True).data
