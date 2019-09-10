"""User model module"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .base_model import CommonFields
from api.models.user_manager import UserManager


class User(AbstractBaseUser, PermissionsMixin, CommonFields):
    """User model """
    USER_TYPE = [
        ('professional', 'professional'),
        ('client', 'client')
    ]
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=30, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    profile_picture = models.CharField(max_length=500, null=True)
    bio = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=30, null=True)
    location = models.CharField(max_length=30, null=True)
    address_1 = models.CharField(max_length=200, null=True)
    address_2 = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    user_type = models.CharField(max_length=20, choices=USER_TYPE, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
   
    class Meta:
        """metadata options."""
        ordering = ('pk',)
        verbose_name = 'User'

    def __str__(self):
        """Return object's string representation."""
        return f'{self.first_name} {self.last_name}'

    @property
    def is_active(self):
        """Check if user is active."""
        return self.active
    
    @property
    def is_staff(self):
        """Check whether user is a staff."""
        return self.staff

    @property
    def is_superuser(self):
        """Check whether user is a super user."""
        return self.admin

    def has_perm(self, perm, obj=None):
        return self.admin
