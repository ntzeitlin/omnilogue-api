from django.db import models
from .story import Story


class StorySection(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="sections")
    file_path = models.TextField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.IntegerField()
    is_start = models.BooleanField(default=False)
    is_end = models.BooleanField(default=False)
