from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Bookshelf(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="bookshelf"
    )


@receiver(post_save, sender=User)
def create_user_bookshelf(instance, created, **kwargs):
    if created:
        Bookshelf.objects.create(user=instance)
