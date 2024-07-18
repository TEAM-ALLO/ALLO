from django.urls import path
from . import views

app_name = "recycle_user"

urlpatterns = [
    path('', views.recycle_main, name='recycle_main'),
    path('<int:pk>', views.recycle_detail, name='recycle_detail'),
]