from django.urls import path
from . import views

app_name = "recycle_user"

urlpatterns = [
    path('recycle/', views.recycle, name='recycle'),
]
