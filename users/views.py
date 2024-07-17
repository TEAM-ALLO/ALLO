from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def home(request):
    return render(request, 'users/home.html')

def signup_view(request):
    if request.method == "POST":
        print(request.POST)
        id = request.POST['id']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']

        errors = {}
        if not id:
            errors['id'] = "아이디를 입력하세요."
        elif User.objects.filter(id=id).exists():
            errors['id'] = "이미 사용중인 아이디입니다."

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

        user = User.objects.create_user(id=id, name=name, email=email, password=password)
        user.save()
        return redirect("users_user:login")
    return render(request, 'users/signup.html')
        
def login_view(request):
    if request.method == "POST":
        id = request.POST["id"]
        password = request.POST["password"]
        user = authenticate(username=id, password=password)
        if user is not None:
            print('인증성공')
            login(request, user)
            return redirect("users_user:home")
        else:
            print('인증실패')
            return render(request, "users/login.html", {'error':'아이디 또는 비밀번호가 잘못되었습니다.'})
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect("users_user:login")