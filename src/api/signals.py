from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import User, Profile

@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):
    """ profile auto-generated everytime a new user is created """
    if instance and created:
        instance.profile = Profile.objects.create(user=instance)
