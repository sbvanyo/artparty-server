"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from artpartyapi.models import Tag


class TagView(ViewSet):
    """Tag view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single tag
        Returns: Response -- JSON serialized tag"""
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all tags
        Returns: Response -- JSON serialized list of tags"""
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""
    class Meta:
        model = Tag
        fields = ('id', 'label')
        depth = 1