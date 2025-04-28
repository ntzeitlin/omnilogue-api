from django.db import models
from django.contrib.auth.models import User


class Bookshelf(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="bookshelf"
    )
