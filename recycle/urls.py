from django.urls import path
from . import views

app_name = "recycle_user"

urlpatterns = [
    path('', views.recycle_main, name='recycle_main'),
    path('list/', views.recycle_list, name='recycle_list'),
]
