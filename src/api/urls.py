from django.urls import path

from api.views import users

register = users.UserViews.as_view({
    'post': 'create'
})
login = users.UserViews.as_view({
    'post': 'login'
})
logout = users.LogoutView.as_view({
    'post': 'logout'
})

home = users.Home.as_view({
    'get': 'index'
})
urlpatterns = [
    path('account/register/', register, name='create-user'),
    path('account/login/', login, name='user-login'),
    path('account/logout/', logout, name='user-logout'),
    path('account/', home, name='home')
]
