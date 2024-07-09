from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import signUpForm, loginForm

def users(request):
    return render(request, 'users_main.html')

def home(request):
    return render(request, 'users/home.html')

def signup(request):
    if request.method == 'POST':
        form = signUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) #사용자 로그인 시키기
            return redirect('home') #회원가입 후 리다이렉션할 url 
    else:
        form = signUpForm()
    return render(request, 'users/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home') #로그인 후 home으로
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form':form})

