from django.db import models
from .story import Story
from .tag import Tag


class StoryTag(models.Model):
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name="story_tags"
    )
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name="tagged_stories"
    )
