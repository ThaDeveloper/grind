"""User manager model module"""
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """User manager model.
    Since our User model overrides the default user
    we need to define a custom manager that extends
    BaseUserManager and defines custom create_user
    and create_superuser methods.
    """
    def create_user(
            self,
            email,
            username,
            password=None,
            is_active=True,
            is_staff=False,
            is_admin=False
        ):
        """Create user."""
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(email=self.normalize_email(email), username=username)
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """Create a superuser."""
        return self.create_user(
            email,
            username,
            is_admin=True,
            is_active=True,
            is_staff=True,
            password=password
        )
