"""
development settings.
"""

import os

from .base import *


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# TODO: add bugsnag error logging middleware
LOGGING = {}

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS', '*')]

STATIC_ROOT = os.environ.get('STATIC_ROOT', '/home/projects/grind/static')
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', '/home/projects/grind/media')
