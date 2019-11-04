from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

from api.serializers import ProfileSerializer
from api.authentication.backends import GrindJWTAuthentication
from api.models import Profile

class ProfileViews(ViewSet):
    """ 
    User Profile Views
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (GrindJWTAuthentication, )
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)


    #TODO: implement cache from django.core.cache import cache
    def retrieve(self, request, username):
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            return Response({
            'status': 'error',
            'error': 'not_found',
            'message': 'A profile for this user does not exist'
        }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(profile, context={
            'request': request
        })

        return Response({
            'status': 'success',
            'data': serializer.data
            }, status=status.HTTP_200_OK)
