from django.urls import path
from . import views

app_name = 'interior_user'

urlpatterns = [
    path('', views.interior_list, name='interior_list'),
    path('post/<int:pk>/', views.interior_detail, name='interior_detail'),
    path('post/new/', views.interior_new, name='interior_new'),
    path('post/<int:pk>/edit/', views.interior_update, name='interior_update'),
    path('post/<int:pk>/delete/', views.interior_delete, name='interior_delete'),
    path('post/<int:pk>/like/', views.like_interior, name='like_interior'),
    path('post/<int:pk>/bookmark/', views.bookmark_interior, name='bookmark_interior'),
    path('bookmarked/', views.bookmarked_interiors, name='bookmarked_interiors'),
]
