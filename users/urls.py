from django.urls import path
from .views import users, home, signup, login

urlpatterns = [
    path('', home, name='home'),
    path('users/', users, name='users'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
]
