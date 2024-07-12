from django.urls import path
from .views import users, home, signup_view, login_view, logout_view

app_name = "user"

urlpatterns = [
    path('', home, name='home'),
    path('users/', users, name='users'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
]