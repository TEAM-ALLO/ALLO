from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Message, Post, EventNotice
from django.contrib.auth.decorators import login_required

def community(request):
    return render(request, 'community/community_main.html')

@login_required
def chat_room(request, username):
    other_user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(sender=request.user, receiver=other_user) | Message.objects.filter(sender=other_user, receiver=request.user)
    messages = messages.order_by('timestamp')
    return render(request, 'community/chat_room.html', {'messages': messages, 'other_user': other_user})

@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        message_text = request.POST.get('message')
        if receiver_username and message_text:
            receiver = get_object_or_404(User, username=receiver_username)
            message = Message(sender=request.user, receiver=receiver, message=message_text)
            message.save()
            return redirect('chat_room', username=receiver_username)
        else:
            # 필요한 인자가 제공되지 않았을 때의 처리
            return redirect('login')
    return redirect('login')

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'community/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'community/post_detail.html', {'post': post})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            post = Post(author=request.user, title=title, content=content)
            post.save()
            return redirect('post_detail', pk=post.pk)
        else:
            # 필요한 인자가 제공되지 않았을 때의 처리
            return redirect('login')
    return render(request, 'community/create_post.html')

def event_list(request):
    events = EventNotice.objects.all().order_by('-event_date')
    return render(request, 'community/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(EventNotice, pk=pk)
    return render(request, 'community/event_detail.html', {'event': event})

@login_required
def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        event_date = request.POST.get('event_date')
        if title and description and event_date:
            event = EventNotice(title=title, description=description, event_date=event_date)
            event.save()
            return redirect('event_detail', pk=event.pk)
        else:
            # 필요한 인자가 제공되지 않았을 때의 처리
            return redirect('login')
    return render(request, 'community/create_event.html')
