from django.db import models
from django.contrib.auth.models import User
from .story import Story


class Bookshelf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookshelf")
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name="bookshelves"
    )
    created_at = models.DateTimeField(auto_now_add=True)
