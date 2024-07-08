from django.shortcuts import render

def users(request):
    return render(request, 'users_main.html')

def home(request):
    return render(request, 'home.html')
