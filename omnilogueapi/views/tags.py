from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from omnilogueapi.models import Tag


class TagViewSet(ViewSet):
    pass


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("name",)
