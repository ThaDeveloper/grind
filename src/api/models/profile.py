"""Profile model module"""
from django.db import models

from api.models.base_model import CommonFields
from api.models import User


class Profile(CommonFields):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    image= models.URLField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)
    address_1 = models.CharField(max_length=200, blank=True)
    address_2 = models.CharField(max_length=200, blank=True)

    class Meta:
        """Define metadata options."""

        ordering = ('pk',)
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username

    @property
    def get_image(self):
        if self.image!="":
            return self.image

        return 'https://static.productionready.io/images/smiley-cyrus.jpg'
