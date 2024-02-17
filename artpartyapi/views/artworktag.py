"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from artpartyapi.models import ArtworkTag


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


class ArtworkTagSerializer(serializers.ModelSerializer):
    """JSON serializer for artworks"""
    class Meta:
        model = ArtworkTag
        fields = ('id', 'artwork', 'tag')
        depth = 1
