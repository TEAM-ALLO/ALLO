from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User

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
        return redirect("user:login")
    return render(request, 'users/signup.html')
        
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            print('인증성공')
            login(request, user)
        else:
            print('인증실패')
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect("user:login")