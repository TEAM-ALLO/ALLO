from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, Notice, ChatRoom, CommunityPost
from .forms import PostForm


def event_list(request):
    events = Event.objects.all()
    return render(request, 'community/event_list.html', {'events': events})

def notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'community/notice_list.html', {'notices': notices})

def chatroom_list(request):
    chatrooms = ChatRoom.objects.all()
    return render(request, 'community/chatroom_list.html', {'chatrooms': chatrooms})

def post_list(request):
    posts = CommunityPost.objects.all()
    return render(request, 'community/post_list.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('community_user:post_list')
    else:
        form = PostForm()
    return render(request, 'community/post_form.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('community_user:post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'community/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)
    if request.user == post.author:
        post.delete()
    return redirect('community_user:post_list')

def like_post(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('community_user:post_list')

@login_required
def bookmark_post(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return redirect('community_user:post_list')

@login_required
def bookmarked_posts(request):
    user = request.user
    posts = CommunityPost.objects.filter(bookmarks=user).order_by('-date_posted')
    return render(request, 'community/bookmarked_posts.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)
    return render(request, 'community/post_detail.html', {'post': post})
