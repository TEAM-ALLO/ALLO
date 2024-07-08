from django.urls import path
from .views import interior

urlpatterns = [
    path('interior/', interior, name='interior'),
]
