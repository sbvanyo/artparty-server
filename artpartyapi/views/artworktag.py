"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from artpartyapi.models import ArtworkTag, Artwork, Tag
from .tag import TagSerializer

class ArtworkTagView(ViewSet):
    """ArtworkTag view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single artworktag
        Returns: Response -- JSON serialized artworktag"""
        try:
            artworktag = ArtworkTag.objects.get(pk=pk)
            serializer = ArtworkTagSerializer(artworktag)
            return Response(serializer.data)
        except ArtworkTag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all artworktags
        Returns: Response -- JSON serialized list of artworktags"""
        artworktags = ArtworkTag.objects.all()
        serializer = ArtworkTagSerializer(artworktags, many=True)
        return Response(serializer.data)


    def create(self, request):
        """Handle POST operations
        Returns Response -- JSON serialized artworktag instance"""
        artwork = Artwork.objects.get(pk=request.data["artwork"])
        tag = Tag.objects.get(pk=request.data["tag"])

        artworktag = ArtworkTag.objects.create(
            artwork=artwork,
            tag=tag,
        )
        serializer = ArtworkTagSerializer(artworktag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def destroy(self, request, pk):
        artworktag = ArtworkTag.objects.get(pk=pk)
        artworktag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class ArtworkTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer()
    """JSON serializer for artworks"""
    class Meta:
        model = ArtworkTag
        fields = ('id', 'artwork', 'tag')
