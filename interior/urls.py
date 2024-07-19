from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from community import views as community_views

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
    path('send_friend_request/<str:username>/', community_views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', community_views.accept_friend_request, name='accept_friend_request'),
    path('decline_friend_request/<int:request_id>/', community_views.decline_friend_request, name='decline_friend_request'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
