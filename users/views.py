from django.shortcuts import render

def users(request):
    return render(request, 'users_main.html')
