from unittest.mock import patch
from django.core import mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from api.helpers.jwt import generate_simple_token
from api.tests.base import BaseTestCase


class TestUserViews(BaseTestCase):
    """ Test user endpoints """

    def test_missing_required_field_fails(self):
        """ Registration fails if username,email, password, first_name,
        last_name, user_type is empty """
        response = self.test_client().post(
            f'/api/v1/accounts/register/', self.blank_user, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            'This field may not be blank.',
            str(response.data['data']['first_name'][0]))
        self.assertEqual(
            'This field may not be blank.',
            str(response.data['data']['last_name'][0]))
        self.assertEqual(
            'This field may not be blank.',
            str(response.data['data']['email'][0]))
        self.assertEqual(
            'This field may not be blank.',
            str(response.data['data']['username'][0]))
        self.assertEqual(
            'This field may not be blank.',
            str(response.data['data']['password'][0]))

    def test_short_password_fails(self):
        """ Test password must be a min of 8 chars long """
        self.new_user['password'] = 'pass'
        response = self.test_client().post(
            f'/api/v1/accounts/register/', self.new_user, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            'Ensure this field has at least 8 characters.',
            str(response.data['data']['password'][0]))

    def test_short_username_fails(self):
        """ Test username must be a min of 5 chars long """
        self.new_user['username'] = 'aa'
        response = self.test_client().post(
            f'/api/v1/accounts/register/', self.new_user, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            'Username must be 5 or more alphabetic characters',
            str(response.data['data']['username'][0]))

    def test_wrong_usertype_fails(self):
        """ Test password must be a min of 8 chars long """
        self.new_user['user_type'] = 'badass'
        response = self.test_client().post(
            f'/api/v1/accounts/register/', self.new_user, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            '"badass" is not a valid choice.',
            str(response.data['data']['user_type'][0]))

    @patch('api.tasks.send_account_email_task.delay')
    def test_registration_success(self, mock_object):
        """ Test user is created successfully and activation email sent """
        response = self.test_client().post('/api/v1/accounts/register/', self.new_user)
        self.assertEqual(201, response.status_code)
        self.assertEqual('Erykah', response.data['data']['first_name'])
        self.assertIn('Registered successfully', response.data['message'])
        assert mock_object.called
        mail_args = mock_object.call_args[0]
        to_email = dict(mail_args[0])['email'][0]
        self.assertEqual(to_email, 'erykah@grind.com')
        assert mail_args[3] == 'Grind - Activate your account'

    def test_activate_user(self):
        """ Test user can activate successully and redirect """
        response = self.create_user(self.new_user)
        email = response.data['data'].get('email')
        response = self.activate_user(email)
        self.assertEqual(302, response.status_code)  # redirects
        self.assertEqual('http://127.0.0.1:8000/?status=success', response.url)

    def test_login_for_inactive_user_fails(self):
        """ Test login fails if user is inactive """
        self.create_user(self.new_user)
        user = {
            'email':  'erykah@grind.com',
            'password':  '@baduism',
        }
        response = self.test_client().post('/api/v1/accounts/login/', user)
        self.assertEqual(400, response.status_code)
        self.assertIn('User is inactive', str(response.data))

    def test_login_success(self):
        """ Test user can login successfully"""
        self.create_user(self.new_user)
        user = {
            'email':  'erykah@grind.com',
            'password':  '@baduism',
        }
        self.activate_user(user.get('email'))
        response = self.test_client().post('/api/v1/accounts/login/', user)
        self.assertEqual(200, response.status_code)
        self.assertIn('Login success', str(response.data))
        self.assertIn('token', str(response.data))

    @patch('api.tasks.send_account_email_task.delay')
    def test_send_reset_request(self, mock_object):
        """ Test user can request password reset """
        email = {
            "email": "erykah@grind.com"
        }
        self.create_user(self.new_user)
        response = self.test_client().post('/api/v1/accounts/send-reset/', email)
        self.assertEqual(200, response.status_code)
        assert mock_object.called
        mail_args = mock_object.call_args[0]
        to_email = dict(mail_args[0])['email'][0]
        self.assertEqual(to_email, 'erykah@grind.com')
        assert mail_args[3] == 'Grind - Password Reset'

    def test_cannot_reset_noexistant_user(self):
        """ Test user reset fails if user is not a memmber """
        email = {
            "email": "missinguser@grind.com"
        }
        response = self.test_client().post('/api/v1/accounts/send-reset/', email)
        self.assertEqual(404, response.status_code)
        self.assertIn('User not found', str(response.data))

    @patch('api.tasks.send_account_email_task.delay')
    def test_can_generate_new_security_link(self, mock_object):
        """ Test user can generate new link after expiry """
        user = {
            "email": "erykah@grind.com",
            "req_type": "activate"
        }
        self.create_user(self.new_user)
        response = self.test_client().post('/api/v1/accounts/new-link/', user)
        self.assertEqual(200, response.status_code)
        assert mock_object.called

    def test_nonexistant_user_link_fails(self):
        """ Test generate new link fails if user does not exist """
        user = {
            "email": "doesnotexist@grind.com",
            "req_type": "activate"
        }
        response = self.test_client().post('/api/v1/accounts/new-link/', user)
        self.assertEqual(404, response.status_code)

    def test_get_user_success(self):
        """ Test can get user profile """
        user = self.create_user(self.new_user)
        username = user.data.get('data').get('username')
        response = self.test_client().get(
            '/api/v1/accounts/{}/profile/'.format(username))
        self.assertEqual(200, response.status_code)
        self.assertEqual('success', response.data['status'])

    def test_get_missing_user_fails(self):
        """ Test cannot get user with wrong username """
        response = self.test_client().get(
            '/api/v1/accounts/m/profile/')
        self.assertEqual(404, response.status_code)
        self.assertIn('User not found', str(response.data))

    def test_update_user_success(self):
        """ Test user can update profile successfully"""
        self.create_user(self.new_user)
        self.activate_user(self.new_user['email'])
        response = self.test_client(
            jwt_token=self.user_token).patch(
            '/api/v1/accounts/profile/update/', self.update_user)
        self.assertEqual(200, response.status_code)
        self.assertIn('Adromeda', str(response.data))

    def test_update_user_unauthenticated_fails(self):
        """ Test user cannot update profile unauthenticated"""
        self.create_user(self.new_user)
        response = self.test_client().patch(
            '/api/v1/accounts/profile/update/', self.update_user)
        self.assertEqual(403, response.status_code)
        self.assertIn("credentials were not provided", str(response.data))

    def test_change_password_success(self):
        """ Test user can change password """
        self.create_user(self.new_user)
        self.activate_user(self.new_user['email'])
        response = self.test_client(
            jwt_token=self.user_token).put(
            '/api/v1/accounts/update-password/', self.passwords)
        self.assertEqual(200, response.status_code)
        self.assertEqual('Password updated successfully',
                         str(response.data['message']))

    def test_unmatching_password_fails(self):
        """ Test change password fails if passwords don't match """
        self.passwords['confirm_password'] = '12234'
        self.create_user(self.new_user)
        self.activate_user(self.new_user['email'])
        response = self.test_client(
            jwt_token=self.user_token).put(
            '/api/v1/accounts/update-password/', self.passwords)
        self.assertEqual(400, response.status_code)
        self.assertIn('Passwords don\'t match',
                      str(response.data))

    def test_password_reset_success(self):
        """ Test user can reset their password """
        self.passwords['password'] = '@baduist'
        self.passwords['confirm_password'] = '@baduist'
        email = self.new_user['email']
        self.create_user(self.new_user)
        self.activate_user(email)
        uid = urlsafe_base64_encode(force_bytes(email))
        token = generate_simple_token(email)
        response = self.test_client().post(
            '/api/v1/accounts/password-reset/{}/{}/'.format(uid, token),
            self.passwords)
        self.assertEqual(200, response.status_code)
        self.assertEqual('Password successfully updated',
                         str(response.data['message']))

    def test_password_reset_fails(self):
        """ Test password reset fails if password isn't strong """
        self.passwords['password'] = 'password'
        self.passwords['confirm_password'] = 'password'
        email = self.new_user['email']
        self.create_user(self.new_user)
        self.activate_user(email)
        uid = urlsafe_base64_encode(force_bytes(email))
        token = generate_simple_token(email)
        response = self.test_client().post(
            '/api/v1/accounts/password-reset/{}/{}/'.format(uid, token),
            self.passwords)
        self.assertEqual(400, response.status_code)
        self.assertIn('This password is too common.',
                      str(response.data))

    def test_user_delete_by_admin_success(self):
        """ Test admin can delete user by Id """
        user = self.create_user(self.new_user)
        pk = user.data['data']['id']
        response = self.test_client(jwt_token=self.admin_token).delete(
            '/api/v1/accounts/{}/delete/'.format(pk))
        self.assertEqual(204, response.status_code)
        self.assertIn('deleted successfully', str(response.data))

    def test_delete_by_non_admin_fails(self):
        """ Test cannot delete user if not an admin """
        user = self.create_user(self.new_user)
        pk = user.data['data']['id']
        self.activate_user(self.new_user['email'])
        response = self.test_client(jwt_token=self.user_token).delete(
            '/api/v1/accounts/{}/delete/'.format(pk))
        self.assertEqual(403, response.status_code)
        self.assertIn(
            'You don\'t have permission to perform this action',
            str(response.data))
