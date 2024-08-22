from django.urls import path
from . import views

app_name = 'community_user'

urlpatterns = [
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/<int:pk>/', views.notice_detail, name='notice_detail'),
    path('notices/create/', views.notice_create, name='notice_create'),
    path('notices/<int:pk>/delete/', views.notice_delete, name='notice_delete'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('chatrooms/', views.chatroom_list, name='chatroom_list'),
    path('chatroom/<int:pk>/<str:username>/', views.chatroom_detail, name='chatroom_detail'),
    path('start_chat/<str:username>/', views.start_chat, name='start_chat'),
    path('send_friend_request/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline_friend_request/<int:request_id>/', views.decline_friend_request, name='decline_friend_request'),
    path('post/', views.post_list, name='post_list'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/update/<int:pk>/', views.post_update, name='post_update'),
    path('post/delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/bookmark/', views.bookmark_post, name='bookmark_post'),
    path('post/bookmarked/', views.bookmarked_posts, name='bookmarked_posts'),
    path('friend/<str:username>/', views.friend, name='friend'),
    path('<int:pk>/', views.comments_create, name='comments_create'),
    path('post/<int:post_id>/comments/<int:comment_id>/delete/', views.comments_delete, name='comments_delete'),
    path('rule/', views.rule_view, name='rule'),
]