from .base import *

DEBUG = False
TESTING = True

INSTALLED_APPS += ('pytest_django',)
TEST_RUNNER = 'api.test_runner.PytestTestRunner'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'grind',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': 5432
    }
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

CORS_ORIGIN_ALLOW_ALL = True

LOGGING = {}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
