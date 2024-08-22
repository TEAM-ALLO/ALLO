from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "recycle_user"

urlpatterns = [
    path('', views.recycle_main, name='recycle_main'),
    path('category/<str:category_name>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('<str:category_name>/<str:item_name>/', views.RecycleDetail.as_view(), name='recycle_detail'),
    path('<str:category_name>/<str:item_name>/edit/', views.RecycleUpdate.as_view(), name='recycle_update'),
    path('<str:category_name>/<str:item_name>/delete/', views.RecycleDelete.as_view(), name='recycle_delete'),
    path('trash/', views.trash, name='trash'),
    path('can/', views.can, name='can'),
    path('paper/', views.paper, name='paper'),
    path('plastic/', views.plastic, name='plastic'),
    path('food/', views.food, name='food'),
    path('vinyl/', views.vinyl, name='vinyl'),
    path('clothing/', views.clothing, name='clothing'),
    path('map/', views.map, name='map'),
    path('create/', views.RecycleCreate.as_view(), name='recycle_create'),
    path('category', views.CategoryDetail.as_view(), name='recycle_category'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)