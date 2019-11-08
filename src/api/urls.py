from django.urls import path

from api.views import users, profiles, social_auth

register = users.UserViews.as_view({
    'post': 'create'
})
activate_user = users.UserViews.as_view({
    'get': 'activate'
})
login = users.UserViews.as_view({
    'post': 'login'
})
logout = users.UserUpdateDestroy.as_view({
    'post': 'logout'
})
update_user = users.UserUpdateDestroy.as_view({
    'patch': 'update'
})
retrieve_profile = profiles.ProfileViews.as_view({
    'get': 'retrieve'
})
# TODO: endpoints to be combined with roles
delete_user = users.UserUpdateDestroy.as_view({
    'delete': 'delete'
})
admin_user_delete = users.UserUpdateDestroy.as_view({
    'delete': 'admin_delete'
})
update_password = users.UpdatePasswordView.as_view({
    'put': 'update'
})
send_reset_email = users.UserViews.as_view({
    'post': 'send_reset_email'
})
password_reset_update = users.UpdatePasswordView.as_view({
    'post': 'password_reset_update'
})
generate_new_link = users.UserViews.as_view({
    'post': 'generate_new_link'
})
fb_auth = social_auth.FacebookAuthAPIView.as_view({
    'post': 'post'
})
google_auth = social_auth.GoogleAuthAPIView.as_view({
    'post': 'post'
})
twitter_auth = social_auth.TwitterAuthAPIView.as_view({
    'post': 'post'
})

urlpatterns = [
    path('accounts/register/', register, name='create-user'),
    path(
        'accounts/activate/<uid>/<token>/', activate_user,
        name='activate-user'),
    path('accounts/login/', login, name='user-login'),
    path('accounts/logout/', logout, name='user-logout'),
    path(
        'accounts/update-password/', update_password, name='update-password'),
    path(
        'accounts/password-reset/', send_reset_email, name='reset-password'),
    path(
        'accounts/send-reset/<uid>/<token>/', password_reset_update,
        name='complete-reset'),
    path(
        'accounts/new-link/', generate_new_link, name='generate-new-link'),
    path(
        'accounts/<username>/profile/', retrieve_profile, name='view-profile'),
    path('accounts/profile/update/', update_user, name='update-user'),
    path(
        'accounts/profile/delete/', delete_user, name='delete-my-account'),
    path('accounts/<pk>/delete/', admin_user_delete, name='admin-delete'),
    path('oauth/facebook/login/', fb_auth, name='facebook-login'),
    path('oauth/google/login/', google_auth, name='google-login'),
    path('oauth/twitter/login/', twitter_auth, name='twitter-login'), ]
