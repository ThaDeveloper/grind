"""
production settings.
"""

import os

from .base import *


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# TODO: add bugsnag error logging middleware
LOGGING = {}

DEBUG = False

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS', '*')]

STATIC_ROOT = os.environ.get('STATIC_ROOT', '/home/projects/grind/static')
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', '/home/projects/grind/media')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
