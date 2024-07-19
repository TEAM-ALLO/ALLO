from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'interior_user'

urlpatterns = [
    path('', views.interior_list, name='interior_list'),
    path('detail/<int:pk>/', views.interior_detail, name='interior_detail'),
    path('new/', views.interior_new, name='interior_new'),
    path('<int:pk>/edit/', views.interior_update, name='interior_update'),
    path('<int:pk>/delete/', views.interior_delete, name='interior_delete'),
    path('<int:pk>/like/', views.like_interior, name='like_interior'),
    path('<int:pk>/bookmark/', views.bookmark_interior, name='bookmark_interior'),
    path('bookmarked/', views.bookmarked_interiors, name='bookmarked_interiors'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
