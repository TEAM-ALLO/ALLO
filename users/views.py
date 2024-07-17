from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.decorators import login_required
from community.models import CommunityPost
from recipe.models import Recipe
from interior.models import InteriorPost
from .forms import CustomUserChangeForm
from django.utils import timezone

def home(request):
    return render(request, 'users/home.html')

def signup_view(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        nickname = request.POST['nickname']
        email = request.POST['email']

        user = User.objects.create_user(username, email, password)
        user.nickname = nickname
        user.save()
        return redirect("users_user:login")
    return render(request, 'users/signup.html')
        
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            today = timezone.now().date()
            if not user.last_login or user.last_login.date() < today:
                user.attendance_score += 1
                user.save()
            print('인증성공')
        else:
            print('인증실패')
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect("users_user:login")

@login_required
def mypage_view(request):
    user = request.user
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
    
    context = {
        'user': user,
        'ranking': ranking[user],
        'community_posts': community_posts,
        'recipe_posts': recipe_posts,
        'interior_posts': interior_posts,
        'community_bookmarks': community_bookmarks,
        'recipe_bookmarks': recipe_bookmarks,
        'interior_bookmarks': interior_bookmarks,
    }
    return render(request, 'users/mypage.html', context)


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users_user:mypage')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})