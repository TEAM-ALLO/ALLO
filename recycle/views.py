from django.views.generic import View, DetailView, CreateView, UpdateView, DeleteView
from .models import Recycle
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from .models import Recycle
from .forms import RecycleForm
import os
from django.db.models import Q

class CategoryDetail(View):
    template_name = 'recycle/recycle_category.html'
    
    def get(self, request, category_name):
        context = {
            'category_name': category_name,
            'recycles': Recycle.objects.filter(category=category_name)
        }
        return render(request, self.template_name, context)
    

def recycle_main(request):
    search_performed = False
    items = []
    if request.method == 'POST':
        query = request.POST.get('query', '')
        if query:
            search_performed = True
            items = Recycle.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
    return render(request, 'recycle/recycle_main.html', {'items': items, 'search_performed': search_performed})

class AuthorRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return HttpResponseForbidden()
        return super(AuthorRequiredMixin, self).dispatch(request, *args, **kwargs)

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
      
class RecycleCreate(StaffRequiredMixin, CreateView):
    model = Recycle
    form_class = RecycleForm
    template_name = 'recycle/recycle_form.html'
    success_url = reverse_lazy('recycle_user:recycle_main')
#self=name(아마 쓰레기 이름ㅇ ㅇ)
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class RecycleDetail(DetailView):
    model = Recycle
    emplate_name = 'recycle/recycle_detail.html'
    
    def get_object(self):
        category_name = self.kwargs.get('category_name')
        item_name = self.kwargs.get('item_name')
        return get_object_or_404(Recycle, category=category_name, name=item_name)

class RecycleUpdate(AuthorRequiredMixin, UpdateView):
    model = Recycle
    form_class = RecycleForm
    template_name = 'recycle/recycle_form.html'

    def get_object(self):
        category_name = self.kwargs.get('category_name')
        item_name = self.kwargs.get('item_name')
        return get_object_or_404(Recycle, category=category_name, name=item_name)
    
    def get_success_url(self):
        return reverse_lazy('recycle_user:recycle_detail', kwargs={
            'category_name': self.object.category,
            'item_name': self.object.name
        })
    
class RecycleDelete(AuthorRequiredMixin, DeleteView):
    model = Recycle
    template_name = 'recycle/recycle_confirm_delete.html'
    
    def get_object(self):
        category_name = self.kwargs.get('category_name')
        item_name = self.kwargs.get('item_name')
        return get_object_or_404(Recycle, category=category_name, name=item_name)
    
    def get_success_url(self):
        return reverse_lazy('recycle_user:category_detail', kwargs={
            'category_name': self.object.category
        })
    
def trash(request):
    return render(request, 'recycle/trash.html')
    
def vinyl(request):
    return render(request, 'recycle/vinyl.html')
    
def can(request):
    return render(request, 'recycle/can.html')
    
def plastic(request):
    return render(request, 'recycle/plastic.html')

def food(request):
    return render(request, 'recycle/food.html')
    
def paper(request):
    return render(request, 'recycle/paper.html')

def clothing(request):
    return render(request, 'recycle/clothing.html')

def map(request):
    context = {
        'kakao_api_key': os.getenv('KAKAO_API_KEY'),
    }
    return render(request, 'recycle/map.html', context)