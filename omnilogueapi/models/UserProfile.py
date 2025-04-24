from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField()
    avatar_link = models.TextField()
    website = models.TextField()
    display_name = models.TextField()
    location = models.TextField()
