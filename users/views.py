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
    recipe_results = Recipe.objects.filter(recipe_name__icontains=query) | Recipe.objects.filter(recipe_name__icontains=query)
    interior_results = InteriorPost.objects.filter(title__icontains=query) | InteriorPost.objects.filter(content__icontains=query)

    context = {
        'query': query,
        'community_results': community_results,
        'recipe_results': recipe_results,
        'interior_results': interior_results,
    }
    return render(request, 'users/searched_list.html', context)




