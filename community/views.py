from django.shortcuts import render, get_object_or_404
from .models import Event, Notice, ChatRoom, CommunityPost

def event_list(request):
    events = Event.objects.all()
    return render(request, 'community/event_list.html', {'events': events})

def notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'community/notice_list.html', {'notices': notices})

def chatroom_list(request):
    chatrooms = ChatRoom.objects.all()
    return render(request, 'community/chatroom_list.html', {'chatrooms': chatrooms})

def post_list(request):
    posts = CommunityPost.objects.all()
    return render(request, 'community/post_list.html', {'posts': posts})
