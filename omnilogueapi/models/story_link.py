from django.db import models
from .story_section import StorySection


class StoryLink(models.Model):
    source_section = models.ForeignKey(
        StorySection, on_delete=models.CASCADE, related_name="link_source"
    )
    target_section = models.ForeignKey(
        StorySection, on_delete=models.CASCADE, related_name="link_target"
    )
    link_text = models.TextField()
