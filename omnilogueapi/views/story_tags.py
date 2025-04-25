from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from omnilogueapi.models import StoryTag
from .tags import TagSerializer


class StoryTagViewSet(ViewSet):
    pass


class StoryTagSerializer(serializers.ModelSerializer):

    tag = TagSerializer(many=False)

    class Meta:
        model = StoryTag
        fields = ("id", "tag")
