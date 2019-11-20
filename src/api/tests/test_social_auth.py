from django.urls import reverse
from unittest.mock import patch

from api.tests.base import BaseTestCase


class SocialTestCase(BaseTestCase):
    def setUp(self):

        self.facebook_token = {
            "access_token": "facebook token"
        }

        self.google_token = {
            "access_token": "google token"
        }
        self.twitter_token = {
            "access_token": "access_token",
            "access_token_secret": "access_token_secret"
        }

        self.return_val = {
            "email": "sample@grind.com", "name": "sample user",
            "first_name": "sample", "last_name": "user"}
        self.facebook_url = reverse("api:facebook-login")
        self.google_url = reverse("api:google-login")
        self.twitter_url = reverse("api:twitter-login")

    @patch('facebook.GraphAPI.get_object')
    def test_facebook_login(self, get_object):
        """ Test user login with facebook """
        get_object.return_value = self.return_val
        self.test_client().post(self.facebook_url, self.facebook_token, format="json")
        response = self.client.post(self.facebook_url,
                                    self.facebook_token, format="json")
        self.assertEqual(response.status_code, 200)

    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_login(self, verify_oauth2_token):
        """Test user login with google."""
        verify_oauth2_token.return_value = self.return_val
        self.test_client().post(self.google_url, self.google_token, format="json")
        response = self.test_client().post(self.google_url, self.google_token,
                                           format="json")
        self.assertEqual(response.status_code, 200)

    @patch('twitter.Api.VerifyCredentials')
    def test_twitter_login(self, verifiedCredentials):
        """ Test user login with twitter """
        verifiedCredentials.return_value.__dict__ = self.return_val
        self.test_client().post(self.twitter_url, self.twitter_token, format="json")
        response = self.test_client().post(
            self.twitter_url, self.twitter_token, format="json")
        self.assertEqual(response.status_code, 200)

    @patch('twitter.Api.VerifyCredentials')
    def test_twitter_login_fail(self, VerifyCredentials):
        """Test user cannot login twitter with wrong token."""
        # note no mock return value assignment(leads to invalid token)
        response=self.client.post(self.twitter_url, self.twitter_token,
                                    format="json")
        self.assertEqual(response.status_code, 400)
