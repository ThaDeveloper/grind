from datetime import datetime, timedelta

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login as auth_login, logout as auth_logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import HttpResponseRedirect
from smtplib import SMTPException
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from api.serializers import (
    UserSerializer, LoginSerializer,
    UpdatePasswordSerializer, PasswordResetSerializer
)
from api.helpers.send_emails import send_account_email
from api.authentication.backends import GrindJWTAuthentication
from api.models import User
from api.helpers.jwt import generate_simple_token

jwt_auth = GrindJWTAuthentication()


class UserViews(ViewSet):
    """ 
    New user registration view
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request):
        """ Register new user and send activation email"""
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                send_acccount_email(
                    request, 'Grind - Activate your account',
                    '/api/v1/accounts/activate/', 'confirm_account.html')
            except (SMTPException, IndexError, TypeError) as e :
                print(e)
                return Response({
                    'status': 'error',
                    'message': 'An error occured, please retry'
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Registered successfully, check your email to activate your account.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'error': 'bad_request',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

    def activate(self, request, uid, token):
        """ Get request for activating user account """
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(email=uid)
            decoded_token = jwt_auth.decode_token(token)
            now = int(datetime.now().strftime('%s'))
            if now > decoded_token['exp']:
                return Response({
                'status': 'error',
                'message': 'Link has expired'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                if user is not None and decoded_token['email'] == user.email:
                    user.active = True
                    user.save()
                    #TODO: update redirect url to web-app login
                    return HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/?status=success')
                else:
                    return Response('Activation link is invalid!')
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'No such user exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError):
            return Response({
                'status': 'error',
                'message': 'An error occured'
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


    def send_reset_email(self, request):
        """ Send password reset email """
        email = request.data.get('email')
        if not email:
            return Response({
                'status': 'error',
                'message': 'Email is required'
            })
        try:
            validate_email(email)
        except ValidationError:
            return Response({
                'status': "error",
                'message': "Invalid Email"
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({
                    'status': 'error',
                    'message': 'No user with such email'
                }, status=status.HTTP_400_BAD_REQUEST)
            send_account_email(
                request, 'Grind - Password Reset',
                '/api/v1/accounts/send-reset/', 'password_reset.html') 
                #TODO: to update link to web-app reset password page
            return Response({
                'status': "success",
                'message': "A reset link has been sent to your email"
            }, status=status.HTTP_200_OK)
        except (SMTPException, IndexError, TypeError):
            return Response({
                'status': 'error',
                'message': 'An error occured, please retry'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateDestroy(ViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (GrindJWTAuthentication,)
    serializer_class = UserSerializer

    def update(self, request):
        user_data = request.data
        serializer_data = {
            'email': user_data.get('email', request.user.email),
            'user_type': user_data.get('user_type', request.user.user_type),

            'profile': {
                'title': user_data.get('title', request.user.profile.title),
                'bio': user_data.get('bio', request.user.profile.bio),
                'image': user_data.get('image', request.user.profile.image),
                'phone': user_data.get('phone', request.user.profile.phone),
                'location': user_data.get('location', request.user.profile.location),
                'address_1': user_data.get('address_1', request.user.profile.address_1),
                'address_2': user_data.get('address_2', request.user.profile.address_2),

            }
        }
        serializer = self.serializer_class(
        request.user, data=serializer_data, partial=True, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Profile updated successfully",
                "data": serializer.data}
                , status=status.HTTP_200_OK)
        return Response({
                "status": "error",
                "error": serializer.errors}
                , status=status.HTTP_400_BAD_REQUEST)


    def logout(self, request):
        auth_logout(request)
        return Response(
            {
                'status': "success",
                'message': "You have been logged out"
            }, status=status.HTTP_204_NO_CONTENT
        )


    def delete(self, request):
        request.user.delete()
        return Response({
            'status': 'success',
            'message': 'Deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


    def admin_delete(self, request, pk):
        if request.user.has_perm:
            try:
                User.objects.get(pk=pk).delete()
                return Response({
                    'status': 'success',
                    'message': 'User ID:{} deleted successfully'.format(pk)
                }, status=status.HTTP_204_NO_CONTENT)
            except User.DoesNotExist:
                return Response({
                'status': 'error',
                'message': 'User ID:{} not found'.format(pk)
            }, status=status.HTTP_404_NOT_FOUND)
        return Response({
                'status': 'error',
                'message': 'You don\'t have permission to perform this action'
            }, status=status.HTTP_403_FORBIDDEN)


class UpdatePasswordView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdatePasswordSerializer

    def update(self, request):
        """ Change password"""
        passwords = request.data
        user = request.user
        serializer = self.serializer_class(data=passwords, context={'request': request})
        if serializer.is_valid():
            user.set_password(passwords.get('new_password'))
            user.save()
            return Response({
                    'status': 'success',
                    'message': 'Password updated successfully'
                }, status=status.HTTP_200_OK)
        return Response({
                    'status': 'error',
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)


    def password_reset_update(self, request, uid, token):
        """ Update the new password to db """
        decoded_token = jwt_auth.decode_token(token)
        now = int(datetime.now().strftime('%s'))
        if now > decoded_token['exp']:
            return Response({
                'status': 'error',
                'message': 'Link has expired'
                }, status=status.HTTP_400_BAD_REQUEST) #TODO: add generate new link endpoint
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                uid = force_text(urlsafe_base64_decode(uid))
                user = User.objects.get(email=uid)
                password = request.data.get('password')
                user.set_password(password)
                user.save()
                return Response({
                    "status": "success",
                    "message": "Password successfully updated"
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({
                    'status': 'error',
                    'message': 'No user with such email'
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'status': 'error',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
