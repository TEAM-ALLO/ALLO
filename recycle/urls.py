from django.urls import path
from . import views

app_name = "recycle_user"

urlpatterns = [
    path('', views.recycle_main, name='recycle_main'),
    path('<int:pk>', views.recycle_detail, name='recycle_detail'),
    path('create/', views.RecycleCreate.as_view(), name='recycle_create'),
    path('<int:pk>/update/', views.RecycleUpdate.as_view(), name='recycle_update'),
    path('<int:pk>/delete/', views.RecycleDelete.as_view(), name='recycle_confirm_delete'),
]