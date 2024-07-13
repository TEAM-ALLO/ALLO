from django.urls import path
from .views import recycle

app_name = "recycle"

urlpatterns = [
    path('recycle/', recycle, name='recycle'),
]
