from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from omnilogueapi.models import Story, Category, StorySection
from .users import UserSerializer
from .categories import CategorySerializer
from .story_tags import StoryTagSerializer
from .story_sections import StorySectionSerializer


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

    def retrieve(self, request, pk=None):
        try:
            story = Story.objects.get(pk=pk)
            serializer = StoryDetailSerializer(story, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Story.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        story = Story()
        story.author = request.user
        story.title = request.data["title"]
        story.subtitle = request.data["subtitle"]
        story.description = request.data["description"]
        story.excerpt = request.data["excerpt"]

        category = Category.objects.get(name=request.data["category"])
        story.category = category
        story.save()

        StorySection.objects.create(
            story=story,
            title=story.title,
            content=request.data["content"],
            order=1,
            file_path="",
        )

        try:
            serializer = StoryDetailSerializer(story, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            story = Story.objects.get(pk=pk)
            story.title = request.data["title"]
            story.subtitle = request.data["subtitle"]
            story.description = request.data["description"]
            story.excerpt = request.data["excerpt"]

            category = Category.objects.get(name=request.data["category"])
            story.category = category
            story.save()

            try:
                story_section = StorySection.objects.get(story=story)
                story_section.content = request.data["content"]
                story_section.save()
            except Exception as ex:
                return Response(
                    {"message": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as ex:
            return HttpResponseServerError(ex)

        return Response("Deleted Successfully", status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            story = Story.objects.get(pk=pk)
            story.delete()
            return Response("Story has been Deleted", status=status.HTTP_200_OK)
        except Story.DoesNotExist:
            return Response(
                {"message": "Story does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# SERIALIZERS:
class StoryOverviewSerializer(serializers.ModelSerializer):
    """JSON Serializer for story overview"""

    author = UserSerializer(many=False, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    story_tags = StoryTagSerializer(many=True)
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = Story
        fields = (
            "id",
            "is_public",
            "author",
            "title",
            "subtitle",
            "category",
            "story_tags",
            "average_rating",
        )


class StoryDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    story_tags = StoryTagSerializer(many=True)
    sections = StorySectionSerializer(many=True)
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = Story
        fields = (
            "id",
            "author",
            "title",
            "subtitle",
            "description",
            "excerpt",
            "category",
            "story_tags",
            "average_rating",
            "sections",
        )
