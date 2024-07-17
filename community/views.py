from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, Notice, ChatRoom, CommunityPost, Message, FriendRequest
from .forms import PostForm, MessageForm
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

def event_list(request):
    events = Event.objects.all()
    return render(request, 'community/event_list.html', {'events': events})

def notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'community/notice_list.html', {'notices': notices})

@login_required
def chatroom_list(request):
    friends = request.user.friends.all()
    return render(request, 'community/chatroom_list.html', {'friends': friends})


@login_required
def chatroom_detail(request, pk):
    chatroom = get_object_or_404(ChatRoom, pk=pk)
    messages = chatroom.messages.all().order_by('timestamp')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chatroom = chatroom
            message.sender = request.user
            message.save()
            return redirect('community_user:chatroom_detail', pk=pk)
    else:
        form = MessageForm()
    return render(request, 'community/chatroom_detail.html', {'chatroom': chatroom, 'messages': messages, 'form': form})


@login_required
def start_chat(request, username):
    other_user = get_object_or_404(User, username=username)
    sorted_usernames = sorted([request.user.username, other_user.username])
    chatroom_name = f'chat_{"_".join(sorted_usernames)}'
    chatroom, created = ChatRoom.objects.get_or_create(name=chatroom_name)
    chatroom.participants.add(request.user, other_user)
    return redirect('community_user:chatroom_detail', pk=chatroom.pk)


@login_required
def send_friend_request(request, username):
    to_user = get_object_or_404(User, username=username)
    if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
        messages.warning(request, '이미 친구 요청을 보냈습니다.')
    else:
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        messages.success(request, '친구 요청을 보냈습니다.')
    return redirect('community_user:post_detail', pk=to_user.username)

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        request.user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(request.user)
        friend_request.delete()
        messages.success(request, '친구 요청을 수락했습니다.')
    else:
        messages.warning(request, '유효하지 않은 요청입니다.')
    return redirect('community_user:friend', username=request.user.username)

@login_required
def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        friend_request.delete()
        messages.success(request, '친구 요청을 거절했습니다.')
    else:
        messages.warning(request, '유효하지 않은 요청입니다.')
    return redirect('community_user:friend', username=request.user.username)

def post_list(request):
    posts = CommunityPost.objects.all()
    return render(request, 'community/post_list.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            request.user.participation_score += 2
            request.user.save()
            return redirect('community_user:post_list')
    else:
        form = PostForm()
    return render(request, 'community/post_form.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('community_user:post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'community/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)
    if request.user == post.author:
        post.delete()
    return redirect('community_user:post_list')

@login_required
def like_post(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)
    if post.likes.filter(username=request.user.username).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        post.author.participation_score += 1
        post.author.save()
    return redirect('community_user:post_detail', pk=pk)

@login_required
def bookmark_post(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)
    if post.bookmarks.filter(username=request.user.username).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return redirect('community_user:post_detail', pk=pk)

@login_required
def bookmarked_posts(request):
    user = request.user
    posts = CommunityPost.objects.filter(bookmarks=user).order_by('-date_posted')
    return render(request, 'community/bookmarked_posts.html', {'posts': posts})

User = get_user_model()

@login_required
def post_detail(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)
    friend_request_sent = FriendRequest.objects.filter(from_user=request.user, to_user=post.author).exists()
    friend_request_received = FriendRequest.objects.filter(from_user=post.author, to_user=request.user).exists()
    friends = request.user.friends.filter(username=post.author.username).exists()
    
    context = {
        'post': post,
        'friend_request_sent': friend_request_sent,
        'friend_request_received': friend_request_received,
        'friends': friends
    }
    
    return render(request, 'community/post_detail.html', context)

@login_required
def friend(request, username):
    user = get_object_or_404(User, username=username)
    received_requests = FriendRequest.objects.filter(to_user=user)
    context = {
        'user': user,
        'received_requests': received_requests
    }
    return render(request, 'community/friend.html', context)
