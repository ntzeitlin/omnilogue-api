from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .stories import StoryOverviewSerializer
from omnilogueapi.models import Story, UserProfile, BookshelfStory

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
        serializer = BookshelfStorySerializer(bookshelf_stories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        bookshelf = request.user.bookshelf

        if request.method == "POST":
            try:
                story_to_add = Story.objects.get(pk=request.data["story_id"])

            except Story.DoesNotExist as ex:
                return Response(
                    {"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND
                )

            except Exception as ex:
                return Response(
                    {"message": ex.args[0]},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            if bookshelf.stories.filter(story=story_to_add):
                return Response(
                    {"message": "Story already in bookshelf"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            BookshelfStory.objects.create(bookshelf=bookshelf, story=story_to_add)
            serializer = BookshelfStorySerializer(bookshelf.stories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            target_story = BookshelfStory.objects.get(
                bookshelf=request.user.bookshelf, story__id=pk
            )
            target_story.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BookshelfStory.DoesNotExist:
            return Response(
                {"message": "Story not found in bookshelf"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as ex:
            return Response(
                {"message": ex.args[0]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# SERIALIZERS
class BookshelfStorySerializer(serializers.ModelSerializer):
    story = StoryOverviewSerializer(many=False)

    class Meta:
        model = BookshelfStory
        fields = ("id", "story")
