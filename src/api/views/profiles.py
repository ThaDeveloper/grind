from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import (
    JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

from api.serializers import UserSerializer
from api.authentication.backends import GrindJWTAuthentication
from api.models import User
from api.helpers.get_response import custom_reponse
from api.helpers.get_object import get_object


class ProfileViews(ViewSet):
    """ 
    User Profile Views
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (GrindJWTAuthentication, )
    serializer_class = UserSerializer
    queryset = User.objects.all()
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

    # TODO: implement cache from django.core.cache import cache

    def retrieve(self, request, username):
        """ Return user profile """
        profile = get_object(User, username, "User")
        serializer = self.serializer_class(profile, context={
            'request': request
        })

        return custom_reponse('success', 200, serializer=serializer)

    def list(self, request):
        """ Return all users """
        serializer = self.serializer_class(
            self.queryset, many=True, context={'request': request})
        return custom_reponse('success', 200, serializer=serializer)
