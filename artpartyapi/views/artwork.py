"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
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
        # Looking at query parameters in the url
        user_id = request.query_params.get('user', None)
        artist_id = request.query_params.get('artist', None)
        featured = request.query_params.get('featured', None)
        
        artworks = Artwork.objects.all()
        
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                artworks = artworks.filter(user=user)
            except User.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if artist_id:
            try:
                artist = Artist.objects.get(id=artist_id)
                artworks = artworks.filter(artist=artist)
            except Artist.DoesNotExist:
                return Response({'message': 'Artist not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if 'featured' query parameter is provided, then filter based on featured status; '.lower() == 'true'' ensures casing isn't an issue
        if featured is not None:  
            artworks = artworks.filter(featured=featured.lower() == 'true')  # 
        
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
    
    
    def update(self, request, pk):
        """Handle PUT requests for an artwork, allowing partial updates.
        Returns: Response -- Empty body with 204 status code"""
        
        artwork = Artwork.objects.get(pk=pk)

        # Update only fields that are provided in the request
        for field in ['title', 'img', 'medium', 'description', 'date', 'age', 'featured']:
            if field in request.data:
                setattr(artwork, field, request.data[field])

        # Only update user and artist if they are explicitly provided
        if 'user' in request.data:
            user = User.objects.get(pk=request.data['user'])
            artwork.user = user

        if 'artist' in request.data:
            artist = Artist.objects.get(pk=request.data['artist'])
            artwork.artist = artist
        
        artwork.save()
    
        # Update tags
        current_tags_ids = set(artwork.tags.values_list('id', flat=True))
        new_tags_ids = set(request.data.get("tags", []))

        # Tags to add
        tags_to_add = new_tags_ids - current_tags_ids
        for tag_id in tags_to_add:
            tag, created = Tag.objects.get_or_create(id=tag_id)
            ArtworkTag.objects.create(artwork=artwork, tag=tag)

        # Tags to remove
        tags_to_remove = current_tags_ids - new_tags_ids
        ArtworkTag.objects.filter(artwork=artwork, tag_id__in=tags_to_remove).delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
    def destroy(self, request, pk):
        artwork = Artwork.objects.get(pk=pk)
        artwork.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

      
      
      
    # Custom actions to add/remove ArtworkTags
     
    @action(methods=['post'], detail=True)
    def add_artwork_tag(self, request, pk):
        """Post request for a user to add an tag to an artwork"""

        tag = Tag.objects.get(pk=request.data["tag"])
        artwork = Artwork.objects.get(pk=pk)
        artworktag = ArtworkTag.objects.create(
            tag=tag,
            artwork=artwork,
        )
        return Response({'message': 'Tag added to artwork'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def remove_artwork_tag(self, request, pk):
        """Delete request for a user to remove an tag from an artwork"""

        artworktag_id = request.data.get("artwork_tag")
        if not artworktag_id:
            return Response({"error": "Artwork tag ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            artwork_tag = ArtworkTag.objects.get(pk=artworktag_id, artwork__pk=pk)
            artwork_tag.delete()
            return Response({"message": "Artwork tag removed"}, status=status.HTTP_204_NO_CONTENT)
        except ArtworkTag.DoesNotExist:
            return Response({"error": "Artwork tag not found"}, status=status.HTTP_404_NOT_FOUND)


class ArtworkSerializer(serializers.ModelSerializer):
    """JSON serializer for artworks"""
    # Value of 'tags' will be computed by 'get_tags' method below
    tags = serializers.SerializerMethodField()
    class Meta:
        model = Artwork
        fields = ('id', 'user', 'artist', 'title', 'img', 'medium', 'description', 'date', 'age', 'featured', 'tags')
        depth = 1
        
    # Serializes artwork tags
    def get_tags(self, artwork):
        """method for getting all tags"""
        # 'tags' coming from related_name='tags' in ArtworkTag model
        artworktags = artwork.tags.all()
        return ArtworkTagSerializer(artworktags, many=True).data
