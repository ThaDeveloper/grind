from rest_framework.response import Response


def custom_reponse(
        status, code, **kwargs):
    """ dynamic response for all json reponses """
    response = {
        'status': status
    }
    serializer = kwargs.get('serializer')
    message = kwargs.get('message')
    error_type = kwargs.get('error_type')
    token = kwargs.get('token')
    if serializer:
        response['data'] = serializer.errors if status == 'error' else serializer.data
    if message:
        response['message'] = message
    if error_type:
        response['error_type'] = error_type
    if token:
        response['token'] = token
    return Response(response, status=code)
