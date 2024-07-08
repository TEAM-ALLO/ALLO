from django.urls import path
from .views import community

urlpatterns = [
    path('community/', community, name='community'),
]
