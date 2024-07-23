from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from .models import Event, Notice, ChatRoom, CommunityPost, Message, FriendRequest, Comment
from .forms import PostForm, MessageForm, CommentForm, EventForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser

User = get_user_model()

def event_list(request):
    events = Event.objects.all()
    return render(request, 'community/event_list.html', {'events': events})

@login_required
@user_passes_test(lambda u: u.is_staff)
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('community_user:event_list')
        
        else:
            print(form.errors)
    else:
        form = EventForm()
    return render(request, 'community/event_form.html', {'form': form})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'community/event_detail.html', {'event': event})

def notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'community/notice_list.html', {'notices': notices})

def notice_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'community/event_detail.html', {'event': event})

@login_required
@user_passes_test(lambda u: u.is_staff)
def notice_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('community_user:notice_list')
        
        else:
            print(form.errors)
    else:
        form = PostForm()
    return render(request, 'community/notice_form.html', {'form': form})


@login_required
def chatroom_list(request):
    friends = request.user.friends.all()
    return render(request, 'community/chatroom_list.html', {'friends': friends})


@login_required
def chatroom_detail(request, pk, username):
    chatroom = get_object_or_404(ChatRoom, pk=pk)
    receiver = get_object_or_404(User, username=username)
    messages = chatroom.messages.all().order_by('timestamp')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chatroom = chatroom
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('community_user:chatroom_detail', pk=pk, username=username)
    else:
        form = MessageForm()
    return render(request, 'community/chatroom_detail.html', {'chatroom': chatroom, 'messages': messages, 'form': form, 'receiver':receiver})


@login_required
def start_chat(request, username):
    other_user = get_object_or_404(User, username=username)
    sorted_usernames = sorted([request.user.username, other_user.username])
    chatroom_name = f'chat_{"_".join(sorted_usernames)}'
    chatroom, created = ChatRoom.objects.get_or_create(name=chatroom_name)
    chatroom.participants.add(request.user, other_user)
    return redirect('community_user:chatroom_detail', pk=chatroom.pk, username=username)


@login_required
def send_friend_request(request, username):
    to_user = get_object_or_404(User, username=username)
    if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
        return JsonResponse({'status': 'error', 'message': '이미 친구 요청을 보냈습니다.'})
    else:
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return JsonResponse({'status': 'success', 'message': '친구 요청을 보냈습니다.'})


@login_required
@require_POST
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        request.user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(request.user)
        friend_request.delete()
        return JsonResponse({'status': 'success', 'message': '친구 요청을 수락했습니다.'})
    return JsonResponse({'status': 'error', 'message': '유효하지 않은 요청입니다.'})

@login_required
@require_POST
def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        friend_request.delete()
        return JsonResponse({'status': 'success', 'message': '친구 요청을 거절했습니다.'})
    return JsonResponse({'status': 'error', 'message': '유효하지 않은 요청입니다.'})


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
        request.user.participation_score -= 2  # 참여 점수 감소
        request.user.save()
        post.delete()
    return redirect('community_user:post_list')


@login_required
def like_post(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)
    
    if isinstance(request.user, AnonymousUser):
        return redirect('users_user:login')
    
    if post.likes.filter(username=request.user.username).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        if post.author is not None:
            post.author.participation_score += 1
            post.author.save()

    return JsonResponse({'liked': liked, 'likes_count': post.total_likes()})

@login_required
def bookmark_post(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)

    if isinstance(request.user, AnonymousUser):
        return redirect('users_user:login')
    
    if post.bookmarks.filter(username=request.user.username).exists():
        post.bookmarks.remove(request.user)
        bookmarked = False
    else:
        post.bookmarks.add(request.user)
        bookmarked = True
        
    return JsonResponse({'bookmarked': bookmarked, 'bookmarks_count':post.total_likes()})

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
    comments = post.comments.all()
    comment_form = CommentForm()

    context = {
        'post': post,
        'friend_request_sent': friend_request_sent,
        'friend_request_received': friend_request_received,
        'friends': friends,
        'comments' : comments,
        'comment_form' : comment_form,
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
    return render(request, 'users/friend.html', context)


@login_required
def liked_posts(request):
    user = request.user
    posts = CommunityPost.objects.filter(likes=user).order_by('-date_posted')
    return render(request, 'community/liked_posts.html', {'posts': posts})

@require_POST
@login_required
def comments_create(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        request.user.participation_score += 1
        request.user.save()

        comments = post.comments.all().values('id', 'user__username', 'content', 'created_at')
        comments_list = list(comments)
    
        return JsonResponse({
            'success': True,
            'comments': comments_list,
            'total_comments': post.comments.count()  # 댓글 총 개수를 반환
        })
    else:
        return JsonResponse({'success': False, 'errors': comment_form.errors})

@require_POST
@login_required
def comments_delete(request, post_id, comment_id):
    post = get_object_or_404(CommunityPost, pk=post_id)
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        request.user.participation_score -= 1  # 참여 점수 감소
        request.user.save()
        comment.delete()

        comments = post.comments.all().values('id', 'user__username', 'content', 'created_at')
        comments_list = list(comments)

        return JsonResponse({
            'success': True,
            'comments': comments_list,
            'total_comments': post.comments.count()  # 댓글 총 개수를 반환
        })
    else:
        return JsonResponse({'success': False, 'message': 'Unauthorized'})