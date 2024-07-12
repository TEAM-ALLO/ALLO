from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.event_list, name='event_list'),
    path('notices/', views.notice_list, name='notice_list'),
    path('chatrooms/', views.chatroom_list, name='chatroom_list'),
    path('posts/', views.post_list, name='post_list'),
]
