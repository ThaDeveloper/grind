""" Common fields module"""
from django.db import models

class CommonFields(models.Model):
    """Add common fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        """metadata options."""
        abstract = True
