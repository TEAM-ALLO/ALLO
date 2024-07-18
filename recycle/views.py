from django.views.generic import TemplateView, DetailView
from django.db.models import Q
from .models import Recycle
from django.shortcuts import render, get_object_or_404

def recycle_main(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        items = Recycle.objects.filter(name__icontains=query)
    else:
        items = []
    return render(request, 'recycle/recycle_main.html', {'items': items})

def recycle_detail(request, pk):
    recycle = get_object_or_404(Recycle, pk=pk)
    return render(request, 'recycle/recycle_detail.html', {'recycle': recycle})
