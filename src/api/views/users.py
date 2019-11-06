from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login as auth_login, logout as auth_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

from api.serializers import UserSerializer, LoginSerializer


class UserViews(ViewSet):
    """ 
    New user registration view
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'error',
            'error': 'bad_request',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            auth_login(request, user)
            return Response(
                {
                    'status': 'success',
                    'token': user.token
                }, status=status.HTTP_200_OK
            )
        return Response(
            {
                'status': 'error',
                'error': 'login_error',
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(ViewSet):
    authentication_classes = (TokenAuthentication,)

    def logout(self, request):
        auth_logout(request)
        return Response(
            {
                'status': "success",
                'message': "You have been logged out"
            }, status=status.HTTP_204
        )
