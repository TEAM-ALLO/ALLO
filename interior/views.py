from django.shortcuts import render, get_object_or_404, redirect
from .models import InteriorPost
from .forms import InteriorPostForm

def interior_list(request):
    posts = InteriorPost.objects.all().order_by('-created_at')
    return render(request, 'interior/interior_list.html', {'posts': posts})

def interior_detail(request, pk):
    post = get_object_or_404(InteriorPost, pk=pk)
    return render(request, 'interior/interior_detail.html', {'post': post})

def interior_new(request):
    if request.method == "POST":
        form = InteriorPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('interior_user:interior_detail', pk=post.pk)
    else:
        form = InteriorPostForm()
    return render(request, 'interior/interior_edit.html', {'form': form})
