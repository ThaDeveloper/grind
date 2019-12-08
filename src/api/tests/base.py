from rest_framework.test import APITestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from api.helpers.jwt import generate_simple_token
from api.models import User


class BaseTestCase(APITestCase):

    def setUp(self):
        self.blank_user = {
            'first_name': "",
            'last_name': "",
            'email':  "",
            'username':  "",
            'password': "",
            'user_type':  ""
        }
        self.new_user = {
            'first_name': "Erykah",
            'last_name': "Badu",
            'email':  "erykah@grind.com",
            'username':  "baduism",
            'password': "@baduism",
            'user_type':  "professional"
        }
        self.update_user = {
            "location": "Adromeda",
            'user_type':  "professional"
        }
        self.passwords = {
            "old_password": "@baduism",
            "new_password": "erykah@123",
            "confirm_password": "erykah@123"
        }
        self.admin = {
            'first_name': "Admin",
            'last_name': "Strator",
            'email':  "admin@grind.com",
            'username':  "admin",
            'password': "@baduism",
            'user_type': "professional",
            'admin': True
        }
        self.user_token = generate_simple_token(self.new_user['email'])
        admin = User.objects.create(**self.admin)
        self.admin_token = admin.token

    def test_client(self, jwt_token=None):
        """ test client with optional auth token """
        client = self.client
        client.credentials()
        if jwt_token:
            client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(jwt_token))
        return client

    def create_user(self, user):
        return self.test_client().post('/api/v1/accounts/register/', user)

    def activate_user(self, email):
        uid = urlsafe_base64_encode(force_bytes(email))
        token = generate_simple_token(email)
        response = self.test_client().get(
            '/api/v1/accounts/activate/{}/{}/'.format(uid, token))
        return response
