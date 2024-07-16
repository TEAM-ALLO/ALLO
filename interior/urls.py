from django.urls import path
from . import views
app_name = 'interior_user'
urlpatterns = [
    path('', views.interior_list, name='interior_list'),
    path('<int:pk>/', views.interior_detail, name='interior_detail'),
    path('new/', views.interior_new, name='interior_new'),
]