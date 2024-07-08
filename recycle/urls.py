from django.urls import path
from .views import recycle

urlpatterns = [
    path('recycle/', recycle, name='recycle'),
]
