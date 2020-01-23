from datetime import datetime, timedelta

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.viewsets import ViewSet
from django.contrib.auth import login as auth_login, logout as auth_logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import HttpResponseRedirect
from smtplib import SMTPException
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from api.serializers import (
    UserSerializer, LoginSerializer,
    UpdatePasswordSerializer, PasswordResetSerializer,
    SecurityLinkSerializer, ResetEmailSerializer
)
from api.authentication.backends import GrindJWTAuthentication
from api.models import User
from api.helpers.jwt import generate_simple_token
from api.helpers.get_response import custom_reponse
from api.helpers.get_object import get_object
from api.tasks import send_account_email_task

jwt_auth = GrindJWTAuthentication()


class UserViews(ViewSet):
    """
    New user registration view
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request):
        """ Register new user and send activation email"""
        serializer = UserSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                data = request.data
                host = request.get_host()
                protocol_secure = request.is_secure()
                send_account_email_task.delay(
                    data, host, protocol_secure,
                    'Grind - Activate your account',
                    '/api/v1/accounts/activate/', 'confirm_account.html')
            except (SMTPException, IndexError, TypeError) as e:
                return custom_reponse(
                    'error', 400, message='An error occured, please retry',
                    error_type='email_error')
            serializer.save()
            return custom_reponse(
                'success', 201, serializer=serializer,
                message='Registered successfully, check your email to activate your account.')
        return custom_reponse('error', 400, serializer=serializer)

    def activate(self, request, uid, token):
        """ Get request for activating user account """
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = get_object(User, uid, "User")
            decoded_token = jwt_auth.decode_token(token)
            now = int(datetime.now().strftime('%s'))
            if now > decoded_token['exp']:
                return custom_reponse('error', 400, message='Link has expired')
            else:
                if user is not None and decoded_token['email'] == user.email:
                    user.active = True
                    user.save()
                    # TODO: update redirect url to web-app login
                    return HttpResponseRedirect(
                        redirect_to='http://127.0.0.1:8000/?status=success')
                else:
                    return custom_reponse(
                        'error', 400, message='Activation link is invalid!')
        except (TypeError, ValueError, OverflowError):
            return custom_reponse('error', 400, message='An error occured')

    def login(self, request):
        serializer = LoginSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            auth_login(request, user)
            return custom_reponse(
                'succes', 200, token=user.token, message='Login success')
        return custom_reponse('error', 400, serializer=serializer,
                              message='login_invalid')

    def send_reset_email(self, request):
        """ Send password reset email """
        serializer = ResetEmailSerializer(data=request.data)
        email = request.data.get('email')
        if serializer.is_valid():
            try:
                get_object(User, email, "User")
                data = request.data
                host = request.get_host()
                protocol_secure = request.is_secure()
                send_account_email_task.delay(
                    data, host, protocol_secure, 'Grind - Password Reset',
                    '/api/v1/accounts/send-reset/', 'password_reset.html')
                # TODO: to update link to web-app reset password page
                return custom_reponse(
                    'success', 200,
                    message="A reset link has been sent to your email")
            except (SMTPException, IndexError, TypeError):
                return custom_reponse(
                    'error', 400, message='An error occured, please retry')
        return custom_reponse('error', 400, serializer=serializer,
                              error_type='bad_request')

    def password_reset_update(self, request, uid, token):
        """ Update the new password to db """
        decoded_token = jwt_auth.decode_token(token)
        now = int(datetime.now().strftime('%s'))
        if now > decoded_token['exp']:
            # TODO: add generate new link endpoint
            return custom_reponse('error', 400, message='Link has expired')
        serializer = PasswordResetSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            uid = force_text(urlsafe_base64_decode(uid))
            user = get_object(User, uid, "User")
            password = request.data.get('password')
            user.set_password(password)
            user.save()
            return custom_reponse(
                'success', 200, message='Password successfully updated')
        return custom_reponse(
            'error', 400, serializer=serializer, error_type='bad_request')

    def generate_new_link(self, request):
        """ Generate new link after expiry """
        email = request.data.get('email')
        req_type = request.data.get('req_type')
        serializer = SecurityLinkSerializer(data=request.data)
        if serializer.is_valid():
            try:
                get_object(User, email, "User")
                if req_type == 'activate':
                    path = '/api/v1/accounts/activate/'
                    subject = 'Grind - Activate your account'
                    template = 'confirm_account.html'
                else:
                    path = '/api/v1/accounts/send-reset/'
                    subject = 'Grind - Password Reset'
                    template = 'password_reset.html'
                data = request.data
                host = request.get_host()
                protocol_secure = request.is_secure()
                send_account_email_task.delay(
                    data, host, protocol_secure, subject,
                    path, template)
                return custom_reponse(
                    'succes', 200,
                    message="A new link has been sent to your email")
            except (SMTPException, IndexError, TypeError):
                return custom_reponse(
                    'error', 400, message='An error occured, please retry')
        return custom_reponse(
            'error', 400, serializer=serializer, error_type='bad_request')


class UserUpdateDestroy(ViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (GrindJWTAuthentication,)
    serializer_class = UserSerializer

    def update(self, request):
        """ Update user profile """
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
            request.user, data=serializer_data, partial=True,
            context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return custom_reponse(
                'succes', 200, message='Profile updated successfully',
                serializer=serializer)
        return custom_reponse('error', 400, serializer=serializer,
                              error_type='bad_request')

    def logout(self, request):
        auth_logout(request)
        return custom_reponse(
            'success', 204, message='You have been logged out')

    def delete(self, request):
        request.user.delete()
        return custom_reponse('success', 204, message='Deleted successfully')

    def admin_delete(self, request, pk):
        """ Delete user by ID """
        if request.user.admin:
            try:
                User.objects.get(pk=pk).delete()
                return custom_reponse(
                    'success', 204,
                    message='User ID:{} deleted successfully'.format(pk))
            except User.DoesNotExist:
                return custom_reponse(
                    'error', 404, message='User ID:{} not found'.format(pk))
        return custom_reponse(
            'error', 403,
            message='You don\'t have permission to perform this action')


class UpdatePasswordView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdatePasswordSerializer

    def update(self, request):
        """ Change password"""
        passwords = request.data
        user = request.user
        serializer = self.serializer_class(
            data=passwords, context={'request': request})
        if serializer.is_valid():
            user.set_password(passwords.get('new_password'))
            user.save()
            return custom_reponse(
                'succes', 200, message='Password updated successfully')
        return custom_reponse(
            'error', 400, serializer=serializer, error_type='bad_request')
