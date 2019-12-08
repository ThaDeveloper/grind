"""User model module"""
import jwt
from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.core.validators import RegexValidator

from .base_model import CommonFields
from api.models.user_manager import UserManager


class User(AbstractBaseUser, PermissionsMixin, CommonFields):
    """User model """
    USER_TYPE = [
        ('professional', 'professional'),
        ('client', 'client')
    ]
    USERNAME_REGEX = '^[a-zA-Z]{5,}$'
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Username must be 5 or more alphabetic characters',
                code='invalid_username')],
        unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    user_type = models.CharField(max_length=20, choices=USER_TYPE, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

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

    @property
    def token(self):
        """
        Get a user's token by calling `user.token`.
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token for access to auth endpoints
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'username': self.username,
            'email': self.email,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def get_full_name(self):
        return ('%s %s') % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.admin
