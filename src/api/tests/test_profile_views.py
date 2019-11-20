from api.tests.base import BaseTestCase


class TestUserViews(BaseTestCase):
    """ Test Profile views """
    def test_get_profile(self):
        """ Test can get single user profile """
        self.create_user(self.new_user)
        response = self.test_client().get('/api/v1/accounts/baduism/profile/')
        self.assertEqual(200, response.status_code)
        self.assertIn("baduism", str(response.data))
    
    def test_get_users(self):
        """ Test can get all users """
        self.create_user(self.new_user)
        response = self.test_client().get('/api/v1/accounts/')
        self.assertEqual(200, response.status_code)
        self.assertIn("baduism", str(response.data))
