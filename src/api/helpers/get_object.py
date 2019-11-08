from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from api.models import User

def get_object(model, value, model_name):
    try:
        return model.objects.get(email=value)
    except model.DoesNotExist:
        raise NotFound({
            'status': 'error',
            'message': '{} not found'.format(model_name)
        })
