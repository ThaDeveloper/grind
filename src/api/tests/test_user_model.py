from rest_framework.test import APITestCase
from api.models.user import User

class TestUserModel(APITestCase):
    """ User model test cases """
    def test_client(self, jwt_token=None):
        """ test client with optional auth token """
        client = self.client
        client.credentials()
        if jwt_token:
            client.credentials(HTTP_AUTHORIZATION=jwt_token)
        return client
    
    def test_create_user_success(self):
        """ Test can add user to db successfully """
        user = User.objects.create(**{
                'first_name': "Erykah",
                'last_name': "Badu",
                'email':  "erykahbadu@email.com",
                'username':  "badu",
                'password': "badu",
                'user_type':  "professional"
            })
        self.assertEqual(user.username, 'badu')

    