from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    community,chat_room,send_message,post_list,post_detail,create_post,
    event_list,event_detail, create_event
    )

urlpatterns = [
    path('chat/<str:username>/', login_required(chat_room), name='chat_room'),
    path('send_message/', login_required(send_message), name='send_message'),
    path('post_list/', post_list, name='post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('create_post/', login_required(create_post), name='create_post'),
    path('', event_list, name='event_list'),
    path('event/<int:pk>/', event_detail, name='event_detail'),
    path('community/create_event/', login_required(create_event), name='create_event'),

]
