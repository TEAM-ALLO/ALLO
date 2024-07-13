from django.urls import path
from .views import interior

app_name = "interior"

urlpatterns = [
    path('interior/', interior, name='interior'),
]
