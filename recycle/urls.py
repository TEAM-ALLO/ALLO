from django.urls import path
from . import views

app_name = "recycle_user"

urlpatterns = [
    path('', views.recycle_main, name='recycle_main'),
    path('category/<str:category_name>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('<int:pk>', views.recycle_detail, name='recycle_detail'),
    path('trash/', views.trash, name='trash'),
    path('can/', views.can, name='can'),
    path('paper/', views.paper, name='paper'),
    path('plastic/', views.plastic, name='plastic'),
    path('food/', views.food, name='food'),
    path('vinyl/', views.vinyl, name='vinyl'),
    path('create/', views.RecycleCreate.as_view(), name='recycle_create'),
    path('<int:pk>/update/', views.RecycleUpdate.as_view(), name='recycle_update'),
    path('<int:pk>/delete/', views.RecycleDelete.as_view(), name='recycle_confirm_delete'),
    path('category', views.CategoryDetail.as_view(), name='recycle_category'),
]