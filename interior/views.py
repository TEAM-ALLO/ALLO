from django.shortcuts import render

def interior(request):
    return render(request, 'interior_main.html')
