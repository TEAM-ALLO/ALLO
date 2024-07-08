from django.shortcuts import render

def community(request):
    return render(request, 'community_main.html')
