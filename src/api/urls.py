from django.urls import path

from api.views import users, profiles

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
#TODO: endpoints to be combined with roles
delete_user = users.UserUpdateDestroy.as_view({
    'delete': 'delete'
})
admin_user_delete = users.UserUpdateDestroy.as_view({
    'delete': 'admin_delete'
})

urlpatterns = [
    path('accounts/register/', register, name='create-user'),
    path('accounts/login/', login, name='user-login'),
    path('accounts/logout/', logout, name='user-logout'),
    path('accounts/<username>/profile', retrieve_profile, name='view-profile'),
    path('accounts/profile/update/', update_user, name='update-user'),
    path('accounts/activate/<uid>/<token>/', activate_user, name='activate-user'),
    path('accounts/profile/delete/', delete_user, name='delete-my-account'),
    path('accounts/<pk>/delete/', admin_user_delete, name='admin-delete'),
]
