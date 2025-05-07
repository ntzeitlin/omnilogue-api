from django.db import models
from .story import Story
from .bookshelf import Bookshelf


class BookshelfStory(models.Model):
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name="bookshelves"
    )
    bookshelf = models.ForeignKey(
        Bookshelf, on_delete=models.CASCADE, related_name="stories"
    )
    created_at = models.DateTimeField(auto_now_add=True)
