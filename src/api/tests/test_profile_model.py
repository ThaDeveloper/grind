from api.models import Profile, User
from api.tests.base import BaseTestCase


class TestUserModel(BaseTestCase):
    """ User model test cases """

    def test_create_user_adds_profile(self):
        """ Test creating user adds a respective profile """
        old_count = Profile.objects.count()
        user = User.objects.create(**{
            'first_name': "Erykah",
            'last_name': "Badu",
            'email':  "erykahbadu@email.com",
            'username':  "badu",
            'password': "badu",
            'user_type':  "professional"
        })
        new_count = Profile.objects.count()
        self.assertEqual(new_count, old_count + 1)
