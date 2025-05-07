from django.db import models
from django.contrib.auth.models import User
from .story import Story


class StoryReadingHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reading_history"
    )
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name="reading_history"
    )
    section_id_list = models.TextField()
