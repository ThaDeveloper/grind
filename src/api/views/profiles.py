from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import (
    JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

from api.serializers import ProfileSerializer
from api.authentication.backends import GrindJWTAuthentication
from api.models import Profile
from api.helpers.get_response import custom_reponse


class ProfileViews(ViewSet):
    """ 
    User Profile Views
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (GrindJWTAuthentication, )
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

    # TODO: implement cache from django.core.cache import cache

    def retrieve(self, request, username):
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            return custom_reponse(
                'error', 404, error_type='not_found',
                message='A profile for this user does not exist')

        serializer = self.serializer_class(profile, context={
            'request': request
        })

        return custom_reponse('success', 200, serializer=serializer)
