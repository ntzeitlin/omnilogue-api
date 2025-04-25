from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from omnilogueapi.models import StorySection


class StorySectionViewSet(ViewSet):
    pass


class StorySectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StorySection
        fields = ("id", "title", "content", "order")
