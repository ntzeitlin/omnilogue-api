from django.db import models
from django.contrib.auth.models import User
from .category import Category


class Story(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="stories_created"
    )
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.TextField()
    description = models.TextField()
    excerpt = models.TextField()
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="stories_in_category"
    )
    is_interactive = models.BooleanField(default=False)

    @property
    def average_rating(self):
        ratings = self.reviews.all()

        if not ratings.exists():
            return None

        total_rating = 0
        for review in ratings:
            total_rating += review.rating

        return round(total_rating / ratings.count(), 2)
