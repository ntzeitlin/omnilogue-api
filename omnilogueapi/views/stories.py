from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from omnilogueapi.models import Story, Category, StorySection
from .users import UserSerializer
from .categories import CategorySerializer
from .story_tags import StoryTagSerializer
from .story_sections import StorySectionSerializer
import re


def process_markdown_title(section_markdown):
    if not section_markdown:
        return "Default Title"

    lines = section_markdown.split("\n")

    header_text = "Default Title"

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("#"):
            if stripped_line.startswith("##"):
                break
            header_text = stripped_line.strip("#").strip()

    return header_text


def process_markdown_links(content, story):
    if not content:
        return ""

    print(f"Processing links for in story {story.id}")

    pattern = r"(\[\[.*?\]\])"

    segments = re.split(pattern, content)

    for index, segment in enumerate(segments):
        if segment.startswith("[[") and segment.endswith("]]"):
            segment_title = segment[2:-2]
            try:
                target_section_id = StorySection.objects.get(
                    story=story, title=segment_title
                ).id
                segments[index] = f"[{segment_title}]({target_section_id})"
            except StorySection.DoesNotExist:
                segments[index] = f"[{segment_title}](not-found)"

    return "".join(segments)


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

        # content should be an array, for each section in the content array, generate a new story section

        story_content = request.data["content"]
        count = 0
        for section in story_content:
            count = count + 1
            section_title = process_markdown_title(section["content"])
            StorySection.objects.create(
                story=story,
                title=section_title,
                content=section["content"],
                order=count,
                file_path="",
            )

        # NOTE: Need to iterate through all sections after ALL sections are created.
        #       Then, go into the section, find the links, find the StorySection that matches the link,
        #       and replace that.

        story_sections = StorySection.objects.filter(story=story)
        for section in story_sections:
            section_to_update = StorySection.objects.get(pk=section.id)
            section_to_update.content = process_markdown_links(section, story)
            section_to_update.save(update_fields=["content"])

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

            story_content = request.data.get("content", [])

            if story_content:
                existing_sections = StorySection.objects.filter(story=story)

            for index, section_data in enumerate(story_content):
                section_id = section_data.get("id", None)

                if section_id:
                    try:
                        section = existing_sections.get(pk=section_id)
                        section.title = process_markdown_title(
                            section_data.get("content", section.content)
                        )
                        # section.save()

                        # # Refetch sections after saving titles
                        # story = Story.objects.get(pk=pk)
                        # existing_sections = StorySection.objects.filter(story=story)
                        # section = existing_sections.get(pk=section_id)
                        section.content = process_markdown_links(
                            section_data.get("content", section.content), story
                        )
                        section.order = index + 1
                        section.save()
                    except StorySection.DoesNotExist:
                        # Create a new section if the ID doesn't exist
                        StorySection.objects.create(
                            story=story,
                            title=section_data.get("title", ""),
                            content=section_data.get("content", ""),
                            order=index + 1,
                            file_path="",
                        )
                else:
                    # Create a new section without ID
                    StorySection.objects.create(
                        story=story,
                        title=section_data.get("title", ""),
                        content=section_data.get("content", ""),
                        order=index + 1,
                        file_path="",
                    )

        except Exception as ex:
            return HttpResponseServerError(ex)

        # GET STORY AGAIN BEFORE SENDING ON
        story = Story.objects.get(pk=pk)
        serializer = StoryDetailSerializer(story, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    start_section = serializers.SerializerMethodField()

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
            "start_section",
        )

    def get_start_section(self, obj):
        try:
            section = obj.sections.get(order=1)
            return StorySectionSerializer(section, many=False).data
        except Exception:
            return None


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
