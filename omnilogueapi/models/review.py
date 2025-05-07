from django.db import models
from django.contrib.auth.models import User
from .story import Story


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
