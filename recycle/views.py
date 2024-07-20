from django.views.generic import View, DetailView, CreateView, UpdateView, DeleteView
from .models import Recycle
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from .models import Recycle
from .forms import RecycleForm


class CategoryDetail(View):
    template_name = 'recycle/recycle_category.html'

    def get(self, request, category_name):
        context = {
            'category_name': category_name,
            'recycles': Recycle.objects.filter(category=category_name)
        }
        return render(request, self.template_name, context)


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
    success_url = reverse_lazy('recycle_user:recycle_main')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class RecycleDetail(DetailView):
    model = Recycle

class RecycleUpdate(AuthorRequiredMixin, UpdateView):
    model = Recycle
    form_class = RecycleForm
    success_url = reverse_lazy('recycle_user:recycle_main')

    def get_queryset(self):
        return Recycle.objects.all()  # 모든 Recycle 객체를 반환합니다.
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class RecycleDelete(AuthorRequiredMixin, DeleteView):
    model = Recycle
    success_url = reverse_lazy('recycle_user:recycle_main')

class CategoryDetail(View):
    template_name = 'recycle/recycle_category.html'

    def get(self, request, category_name):
        context = {
            'category_name': category_name,
            'recycles': Recycle.objects.filter(category=category_name, is_in_category=True)
        }
        return render(request, self.template_name, context)
    
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