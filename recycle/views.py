from django.shortcuts import render
from .models import Recycle

def recycle_main(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        items = Recycle.objects.filter(name__icontains=query)
    else:
        items = []
    return render(request, 'recycle/recycle_main.html', {'items': items})

def recycle_list(request):
    items = Recycle.objects.all()
    return render(request, 'recycle/recycle_list.html', {'items': items})