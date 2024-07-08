from django.urls import path
from .views import users,home

urlpatterns = [
    path('', home, name='home'),
    path('users/', users, name='users'),
]
