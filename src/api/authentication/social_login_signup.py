import uuid

from rest_framework.response import Response
from rest_framework import status

from api.models import User
from api.helpers.get_response import custom_reponse


class SocialAuth:
    """
    Logs in/ registers a new social user.
    """

    def social_login_signup(self, user_info, **kwargs):
        """
        If user exists, authenticate user with their `social account` info
        else register user using their `social accounts`
        info.
        Returns: API access token and/or user data.
        """
        try:
            user = User.objects.get(email=user_info.get('email'))
            token = user.token
            return custom_reponse('success', 200, toke=token,
                                  message='Logged in successfully.')
        except User.DoesNotExist:
            password = User.objects.make_random_password()
            user = User(
                username=str(user_info.get('first_name')) +
                str(uuid.uuid1().int)[: 3],
                email=user_info.get('email'),
                first_name=user_info.get('first_name'),
                last_name=user_info.get('last_name'),
                active=True)
            user.set_password(password)
            user.save()
            user_details = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
            token = user.token
            return Response({
                'status': 'success',
                'token': token,
                'data': user_details,
                'message': 'Account created successfully '
            }, status=status.HTTP_201_CREATED)
