import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from .models import User
from community.models import FriendRequest
from django.contrib.auth.decorators import login_required
from community.models import CommunityPost
from recipe.models import Recipe
from interior.models import InteriorPost
from .forms import CustomUserChangeForm
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
import datetime
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_POST
from .models import Notification


def home(request):
    all_users = User.objects.all()
    sorted_users = sorted(all_users, key=lambda u: (u.attendance_score + u.participation_score), reverse=True)
    # first=sorted_users[0]
    # second=sorted_users[1]
    # third=sorted_users[2]

    # context = {
    #     'first': first,
    #     'second': second,
    #     'third': third,
    
    # }
    top_users = []
    for user in sorted_users[:3]:
        score = user.attendance_score + user.participation_score
        top_users.append({'username': user.username, 'score': score, 'name':user.name, 'profile_image':user.profile_image})
    
    context = {
        'top_users': top_users,
    }
    return render(request, 'users/home.html', context)

def signup_view(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']

        errors = {}
        if not username:
            errors['username'] = "아이디를 입력하세요."
        elif User.objects.filter(username=username).exists():
            errors['username'] = "이미 사용중인 아이디입니다."

        if not password:
            errors['password'] = "비밀번호를 입력하세요."

        if not name:
            errors['name'] = "이름을 입력하세요."

        if not email:
            errors['email'] = "이메일을 입력하세요."
        else:
            try:
                validate_email(email)
                if User.objects.filter(email=email).exists():
                    errors['email'] = "이미 사용중인 이메일입니다."
            except ValidationError:
                errors['email'] = "유효한 이메일을 입력하세요."
                
        if errors:
            return render(request, 'users/signup.html', {'errors': errors})

        user = User.objects.create_user(username=username, name=name, email=email, password=password)
        user.save()
        return redirect("users_user:login")
    return render(request, 'users/signup.html')
        
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            today = timezone.now().date()
            print(f"User last attendance date: {user.last_attendance_date}")
            if user.last_attendance_date != today:
                user.attendance_score += 1
                user.last_attendance_date = today
                user.save()
                print(f"Attendance score updated to: {user.attendance_score}")
            else:
                print("Attendance score not updated.")
            auth_login(request, user)
            print('인증성공')
            return redirect("users_user:home")
        else:
            print('인증실패')
            return render(request, "users/login.html", {'error':'아이디 또는 비밀번호가 잘못되었습니다.'})
    return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    return redirect("users_user:login")

@login_required
def mypage_view(request):
    user = request.user
    context = {}

    if request.method == "POST":
        # 비밀번호 변경 처리
        current_password = request.POST.get("origin_password")
        if check_password(current_password, user.password):
            new_password = request.POST.get("password1")
            password_confirm = request.POST.get("password2")
            if new_password == password_confirm:
                user.set_password(new_password)
                user.save()
                auth_login(request, user)
                context.update({'password_change_success': "비밀번호가 성공적으로 변경되었습니다."})
                return redirect("users_user:home")
            else:
                context.update({'error': "새로운 비밀번호를 다시 확인해주세요."})
        else:
            context.update({'error': "현재 비밀번호가 일치하지 않습니다."})

    # 마이페이지 조회 처리
    community_posts = CommunityPost.objects.filter(author=user)
    recipe_posts = Recipe.objects.filter(author=user)
    interior_posts = InteriorPost.objects.filter(author=user)

    community_bookmarks = CommunityPost.objects.filter(bookmarks=user)
    recipe_bookmarks = Recipe.objects.filter(bookmarks=user)
    interior_bookmarks = InteriorPost.objects.filter(bookmarks=user)

    # 모든 사용자들의 점수를 계산하여 랭킹을 매김
    all_users = User.objects.all()
    sorted_users = sorted(all_users, key=lambda u: (u.attendance_score + u.participation_score), reverse=True)
    ranking = {user: rank+1 for rank, user in enumerate(sorted_users)}

    today = datetime.date.today()

    context.update({
        'user': user,
        'ranking': ranking[user],
        'community_posts': community_posts,
        'recipe_posts': recipe_posts,
        'interior_posts': interior_posts,
        'community_bookmarks': community_bookmarks,
        'recipe_bookmarks': recipe_bookmarks,
        'interior_bookmarks': interior_bookmarks,
        'today': today,
    })

    return render(request, 'users/mypage.html', context)

from django.http import JsonResponse

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        print('POST data:', request.POST)  # 디버깅을 위해 POST 데이터 출력
        print('FILES data:', request.FILES)  # 디버깅을 위해 FILES 데이터 출력
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필이 성공적으로 업데이트되었습니다.')
            return JsonResponse({'status': 'success'})
        else:
            print('Form is not valid')
            print(form.errors)  # 폼 에러 출력
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'invalid request'}, status=400)



@login_required
def friend_list(request, username):
    user = get_object_or_404(User, username=username)
    friends = user.friends.all()
    received_requests = FriendRequest.objects.filter(to_user=user)
    return render(request, 'users/friend.html', {'friends': friends, 'user': user, 'received_requests': received_requests})


@login_required
def friend_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    all_users = User.objects.all()
    sorted_users = sorted(all_users, key=lambda u: (u.attendance_score + u.participation_score), reverse=True)
    ranking = {user: rank+1 for rank, user in enumerate(sorted_users)}
    
    context = {
        'user': user,
        'ranking': ranking[user],
    }
    return render(request, 'users/friend_profile.html', context)

@login_required
def delete_friend(request, username):
    friend = get_object_or_404(User, username=username)
    if friend in request.user.friends.all():
        request.user.friends.remove(friend)
        friend.friends.remove(request.user)
        messages.success(request, f'{friend.username}님을 친구 목록에서 삭제했습니다.')
    else:
        messages.warning(request, '유효하지 않은 요청입니다.')
    return redirect('users_user:friend_list', username=request.user.username)

def search(request):
    query = request.GET.get('q', '')
    community_results = CommunityPost.objects.filter(title__icontains=query) | CommunityPost.objects.filter(content__icontains=query)
    recipe_results = Recipe.objects.filter(recipe_name__icontains=query) | Recipe.objects.filter(ingredients__icontains=query)
    interior_results = InteriorPost.objects.filter(title__icontains=query) | InteriorPost.objects.filter(content__icontains=query)

    context = {
        'query': query,
        'community_results': community_results,
        'recipe_results': recipe_results,
        'interior_results': interior_results,
    }
    return render(request, 'users/searched_list.html', context)


@login_required
def notification(request):
    notifications = request.user.notifications.all()  # 모든 알람을 가져옴
    notification_list = []

    for notification in notifications:
        message = ""
        link = "#"
        
        if notification.notification_type == 'friend_request':
            message = f"{notification.sender.username}님이 친구 요청을 보냈습니다."
            link = f"/friend/{request.user.username}/"  # 친구 요청에 대한 링크를 알림을 받은 사용자의 페이지로 설정
        elif notification.notification_type == 'like' or notification.notification_type == 'comment':
            if notification.content_type.model == 'communitypost':
                link = f"/community/post/{notification.object_id}/"
                message = f"{notification.sender.username}님이 커뮤니티 게시글에 {'좋아요를 눌렀습니다' if notification.notification_type == 'like' else '댓글을 남겼습니다'}."
            elif notification.content_type.model == 'recipe':
                link = f"/recipe/{notification.object_id}/"
                message = f"{notification.sender.username}님이 레시피에 {'좋아요를 눌렀습니다' if notification.notification_type == 'like' else '댓글을 남겼습니다'}."
            elif notification.content_type.model == 'interiorpost':
                link = f"/interior/detail/{notification.object_id}/"
                message = f"{notification.sender.username}님이 인테리어 게시글에 {'좋아요를 눌렀습니다' if notification.notification_type == 'like' else '댓글을 남겼습니다'}."
        elif notification.notification_type == 'message':
            link = f"/chatroom/{notification.object_id}/"  # 메시지 링크
            message = f"{notification.sender.username}님으로부터 새로운 메시지가 도착했습니다."

        notification_list.append({
            'notification': notification,
            'message': message,
            'timestamp': notification.timestamp.strftime('%Y년 %m월 %d일 %I:%M %p'),
            'is_read': notification.is_read,
            'link': link  # 링크 추가
        })

    return render(request, 'users/notification.html', {'notifications': notification_list})

@login_required
@require_POST
def mark_notifications_as_read(request):
    try:
        # 요청에서 전달된 데이터를 직접 출력해 확인합니다.
        print("Request body:", request.body)

        # 요청에서 전달된 notification_ids를 추출합니다.
        notification_ids = json.loads(request.body).get('notification_ids', [])
        print("Received notification IDs:", notification_ids)  # 전달된 ID를 확인합니다.

        # 전달된 notification_ids에 해당하는 알림을 필터링합니다.
        notifications = Notification.objects.filter(id__in=notification_ids, user=request.user)
        
        if notifications.exists():
            notifications.update(is_read=True)
            print("Notifications updated to read:", notifications)  # 읽음으로 업데이트된 알림을 확인합니다.
            return JsonResponse({'status': 'success'})
        else:
            print("Notification not found for user:", request.user)  # 알림을 찾지 못했을 때의 로그
            return JsonResponse({'status': 'error', 'message': 'Notification not found'})
    except Exception as e:
        print("Error processing request:", e)
        return JsonResponse({'status': 'error', 'message': str(e)})



from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_notification_to_user(user, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",  # 사용자 ID를 기반으로 그룹 이름을 지정
        {
            "type": "send_notification",  # 컨슈머에서 실행할 메서드 이름
            "message": message,
        },
    )
