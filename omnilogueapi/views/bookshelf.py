from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from omnilogueapi.models import Story, UserProfile, BookshelfStory
from .stories import StoryOverviewSerializer

# ViewSet to handle GET, PUT, DELETE from bookshelf
# Bookshelf View
# GET -> Return user's bookshelf. If no bookshelf exists for the user, create an empty one. /bookshelves
#   Use the token to pull the proper bookshelf
# PUT -> Add a book to the bookshelf
# DELETE -> Remove book from the bookshelf


class BookshelfViewSet(ViewSet):
    def list(self, request):
        current_user = UserProfile.objects.get(user=request.auth.user)
        bookshelf_stories = current_user.user.bookshelf.stories
        serializer = BookshelfSerializer(bookshelf_stories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# SERIALIZERS
class BookshelfSerializer(serializers.ModelSerializer):
    story = StoryOverviewSerializer(many=False)

    class Meta:
        model = BookshelfStory
        fields = ("id", "story")
