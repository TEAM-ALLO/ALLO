from django.shortcuts import render, get_object_or_404, redirect
from .models import InteriorPost
from .forms import InteriorPostForm
from django.contrib.auth.decorators import login_required

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
            request.user.participation_score += 2
            request.user.save()
            return redirect('interior_user:interior_detail', pk=post.pk)
    else:
        form = InteriorPostForm()
    return render(request, 'interior/interior_edit.html', {'form': form})

@login_required
def interior_update(request, pk):
    post = get_object_or_404(InteriorPost, pk=pk)
    if request.method == 'POST':
        form = InteriorPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('interior_user:interior_list')
    else:
        form = InteriorPostForm(instance=post)
    return render(request, 'interior/post_form.html', {'form': form})

@login_required
def interior_delete(request, pk):
    post = get_object_or_404(InteriorPost, pk=pk)
    if request.user == post.author:
        post.delete()
    return redirect('interior_user:interior_list')

def like_interior(request, pk):
    post = get_object_or_404(InteriorPost, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        post.author.participation_score += 1
        post.author.save()
    return redirect('interior_user:interior_list')

@login_required
def bookmark_interior(request, pk):
    post = get_object_or_404(InteriorPost, pk=pk)
    if post.bookmarks.filter(username=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return redirect('interior_user:interior_list')

@login_required
def bookmarked_interiors(request):
    user = request.user
    posts = InteriorPost.objects.filter(bookmarks=user).order_by('-date_posted')
    return render(request, 'interior/bookmarked_interiors.html', {'posts': posts})

