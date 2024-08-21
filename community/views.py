from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from .models import Event, Notice, ChatRoom, CommunityPost, Message, FriendRequest, Comment
from .forms import PostForm, MessageForm, CommentForm, EventForm, NoticeForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser
import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Notification
from django.contrib.contenttypes.models import ContentType

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
    notice = get_object_or_404(Notice, pk=pk)  
    return render(request, 'community/notice_detail.html', {'notice': notice})
@login_required
@user_passes_test(lambda u: u.is_staff)
def notice_create(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('community_user:notice_list')
        else:
            print(form.errors)
    else:
        form = NoticeForm()
    return render(request, 'community/notice_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    notice.delete()
    return redirect('community_user:notice_list')

@login_required
@user_passes_test(lambda u: u.is_staff)
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return redirect('community_user:event_list')


@login_required
def chatroom_list(request):
    friends = request.user.friends.all()
    return render(request, 'community/chatroom_list.html', {'friends': friends})



@login_required
def chatroom_detail(request, pk, username):
    chatroom = get_object_or_404(ChatRoom, pk=pk)
    receiver = get_object_or_404(User, username=username)
    messages = chatroom.messages.all().order_by('timestamp')

    # Long Polling 처리
    if request.GET.get('ajax'):
        last_message_id = request.GET.get('last_message_id')
        if last_message_id == "null" or last_message_id is None:
            last_message_id = 0  # 모든 메시지를 가져오도록 설정
        else:
            last_message_id = int(last_message_id)

        timeout = 30  # 30초 타임아웃
        start_time = time.time()

        while True:
            new_messages = messages.filter(id__gt=last_message_id)
            if new_messages.exists():
                return JsonResponse({
                    'new_messages': [
                        {
                            'id': msg.id,
                            'sender': msg.sender.username,
                            'content': msg.content,
                            'image': msg.image.url if msg.image else None,
                            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                        } for msg in new_messages
                    ]
                })

            if time.time() - start_time > timeout:
                return JsonResponse({'new_messages': []})

            time.sleep(1)

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.chatroom = chatroom
            message.sender = request.user
            message.receiver = receiver
            message.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': message.id,
                    'sender': message.sender.username,
                    'content': message.content,
                    'image': message.image.url if message.image else None,
                    'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'receiver_profile_image': message.receiver.profile_image.url if message.receiver.profile_image else None,
                })

            return redirect('community_user:chatroom_detail', pk=pk, username=username)
    else:
        form = MessageForm()

    return render(request, 'community/chatroom_detail.html', {
        'chatroom': chatroom,
        'messages': messages,
        'form': form,
        'receiver': receiver
    })


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
        friend_request = FriendRequest.objects.create(from_user=request.user, to_user=to_user)

        # 알림 생성 로직 추가
        Notification.objects.create(
            user=to_user,  # 알림을 받을 사용자 (친구 요청을 받은 사용자)
            sender=request.user,  # 알림을 보낸 사용자 (친구 요청을 보낸 사용자)
            notification_type='friend_request',  # 알림 타입
            content_type=ContentType.objects.get_for_model(friend_request),  # 관련된 모델의 ContentType
            object_id=friend_request.id  # 알림과 관련된 객체의 ID
        )

        return JsonResponse({'status': 'success', 'message': '친구 요청을 보냈습니다.'})

@login_required
@require_POST
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        request.user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(request.user)
        friend_request.delete()
        
        # 친구 정보를 JSON으로 반환
        friend_info = {
            'username': friend_request.from_user.username,
            'profile_url': f'/profile/{friend_request.from_user.username}/'  # URL 패턴에 맞게 조정
        }
        return JsonResponse({'status': 'success', 'message': '친구 요청을 수락했습니다.', 'friend': friend_info})
    
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
        form = PostForm(request.POST, request.FILES)
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
        form = PostForm(request.POST, request.FILES, instance=post)
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


from django.contrib.contenttypes.models import ContentType

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

            # 알림 생성
            Notification.objects.create(
                user=post.author,
                sender=request.user,
                notification_type='like',
                content_type=ContentType.objects.get_for_model(post),
                object_id=post.pk
            )

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
        
    return JsonResponse({'bookmarked': bookmarked, 'bookmarks_count':post.total_bookmarks()})

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
    

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.post.author,  # 댓글이 달린 게시글의 작성자에게 알림
            sender=instance.user,  # 댓글을 단 사용자
            notification_type='comment',
            content_type=ContentType.objects.get_for_model(instance.post),
            object_id=instance.post.pk
        )

@receiver(post_save, sender=CommunityPost)
def create_like_notification(sender, instance, created, **kwargs):
    if not created and instance.likes.exists():
        last_like_user = instance.likes.order_by('-id').first()
        Notification.objects.create(
            user=instance.author,
            sender=last_like_user,
            notification_type='like',
            post=instance
        )


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            sender=instance.sender,
            notification_type='message',
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk
        )
