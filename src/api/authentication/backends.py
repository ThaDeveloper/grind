import jwt

from django.conf import settings
from rest_framework import authentication, exceptions, status
from rest_framework.response import Response

from api.models import User


class GrindJWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        """
        The `authenticate` method is called on every request regardless of
        whether the endpoint requires authentication. 

        Returns:
            `None`: When no authentication fails or not needed
            `(user, token): On successful authenticaion
        """
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) != 2:
            # Invalid token header. No credentials provided or wrong format. Do not attempt to
            # authenticate.
            raise exceptions.AuthenticationFailed({
                "status": "error",
                "message": "Wrong header format"},
                status.HTTP_400_BAD_REQUEST
                )

        # since python3 uses byte we have two decode the two header values
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            # The auth header prefix is not what we expected. Do not attempt to
            # authenticate.
            raise exceptions.AuthenticationFailed({
                "status": "error",
                "message": "Token should be prefixed with `Bearer`"},
                status.HTTP_400_BAD_REQUEST
                )

        # By now, we are confident authentication will succeed to we pass the 
        # credentials to the method below
        #set session
        request.session['grind-jwt-token'] = token
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        Try to authenticate the given credentials.
        If success: return the user and token.
        If fails: throw an error.
        """
    
        payload = self.decode_token(token)
        try:
            user = User.objects.get(email=payload['email'])
            if not user.is_active:
                data = {
                    'status': "error",
                    'message': "User is inactive."
                }
                raise exceptions.AuthenticationFailed(data, status.HTTP_400_BAD_REQUEST)

            return (user, token)
        except User.DoesNotExist:
            data = {
                'status': "error",
                'message': "No user matching credentials was found."
            }
            raise exceptions.AuthenticationFailed(data, status.HTTP_400_BAD_REQUEST)
    
    def decode_token(self, token):
        """Decode token with secret."""
        try:
            return jwt.decode(token,
                            settings.SECRET_KEY,
                            algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            data = {
                'status': 'error',
                'error': 'token_expired',
                'message': 'Login again'
            }
            raise exceptions.AuthenticationFailed(
                data, status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.InvalidTokenError:
            data = {
                'status': 'error',
                'error': 'Invalid token',
                'message': 'Ensure you are using a valid token'
            }
            raise exceptions.AuthenticationFailed(
                data, status.HTTP_400_BAD_REQUEST)
