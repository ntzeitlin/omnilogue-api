from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from omnilogueapi.models import Story
from .users import UserSerializer

# ViewSet to handle GET, PUT, DELETE from bookshelf
# Bookshelf View
# GET -> Return user's bookshelf. If no bookshelf exists for the user, create an empty one. /bookshelves
#   Use the token to pull the proper bookshelf
# PUT -> Add a book to the bookshelf
# DELETE -> Remove book from the bookshelf


class BookshelfViewSet(ViewSet):
    pass
