import facebook
import twitter

from google.oauth2 import id_token
from google.auth.transport import requests
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import exceptions
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from django.conf import settings

from api.authentication.social_login_signup import SocialAuth
from api.serializers import SocialSerializer
from api.helpers.get_response import custom_reponse
from api.helpers.social_user_info import get_user_info


class FacebookAuthAPIView(ViewSet):
    """ Facebook Auth """
    permission_classes = (AllowAny,)
    serializer_class = SocialSerializer

    def post(self, request, **kwargs):
        """
        POST: /api/v1/ouath/facebook/login/
        Register or login user if exists
        Returns: user token and/or user data
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.data.get('access_token')
        try:
            facebook_user = facebook.GraphAPI(access_token=access_token)
            user_info = facebook_user.get_object(
                id='me', fields='name, id, email, first_name, last_name')
        except:
            return custom_reponse('error', 400, message='Invalid token.')
        facebook_auth = SocialAuth()
        return facebook_auth.social_login_signup(
            user_info, **kwargs)


class GoogleAuthAPIView(ViewSet):
    """ Google Auth """
    permission_classes = (AllowAny,)
    serializer_class = SocialSerializer

    def post(self, request, **kwargs):
        """
        POST: /api/v1/ouath/google/login/
        Register or login user if exists
        Returns: user token and/or user data
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.data.get('access_token')
        try:
            user_info = id_token.verify_oauth2_token(
                access_token, requests.Request())
            user_info = get_user_info(user_info)
        except:
            return custom_reponse('error', 400, message='Invalid token.')
        google_auth = SocialAuth()
        return google_auth.social_login_signup(user_info, **kwargs)


class TwitterAuthAPIView(ViewSet):
    """
    Twitter AUth
    """
    permission_classes = (AllowAny,)
    serializer_class = SocialSerializer

    def post(self, request, **kwargs):
        """
        POST: /api/v1/ouath/twitter/login/
        Register or login user if exists
        Returns: user token and/or user data
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token_key = serializer.data.get('access_token')
        access_token_secret = serializer.data.get('access_token_secret')
        try:
            consumer_key = settings.TWITTER_CONSUMER_KEY
            consumer_secret = settings.TWITTER_CONSUMER_SECRET
            api = twitter.Api(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token_key=access_token_key,
                access_token_secret=access_token_secret
            )
            user_info = api.VerifyCredentials(include_email=True)
            user_info = user_info.__dict__
            user_info = get_user_info(user_info)
        except:
            return custom_reponse('error', 400, message='Invalid token.')
        twitter_social_authentication = SocialAuth()
        return twitter_social_authentication.social_login_signup(
            user_info, **kwargs)
