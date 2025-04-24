from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from omnilogueapi.models import Story
from .users import UserSerializer


class StoryViewSet(ViewSet):
    def list(self, request):
        """Handle GET requests for Stories

        Returns:
            Response -- JSON serialized array
        """
        try:
            stories = Story.objects.all()
            serializer = StoryOverviewSerializer(stories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class StoryOverviewSerializer(serializers.ModelSerializer):
    """JSON Serializer for story overview"""

    author = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Story
        fields = ("id", "author", "title", "subtitle", "category", "story_tags")
