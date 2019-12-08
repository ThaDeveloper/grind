from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.db.models import Q

from api.models import User


def get_object(model, value, model_name):
    try:
        return model.objects.get(
            Q(email=value) | Q(username=value) |
            Q(pk=value if isinstance(value, int) else None))
    except model.DoesNotExist:
        raise NotFound({
            'status': 'error',
            'message': '{} not found'.format(model_name)
        })
