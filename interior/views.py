from django.shortcuts import render, get_object_or_404, redirect
from .models import InteriorPost, InteriorComment
from community.models import FriendRequest
from .forms import InteriorPostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from .forms import CommentForm
from django.views.decorators.http import require_POST


def interior_list(request):
    category = request.GET.get('category', 'all')
    if category == 'all':
        posts = InteriorPost.objects.all().order_by('-created_at')
    else:
        posts = InteriorPost.objects.filter(category=category).order_by('-created_at')
    return render(request, 'interior/interior_list.html', {'posts': posts, 'category': category})

@login_required
def interior_detail(request, pk):
    post = get_object_or_404(InteriorPost, pk=pk)
    friend_request_sent = FriendRequest.objects.filter(from_user=request.user, to_user=post.author).exists()
    friend_request_received = FriendRequest.objects.filter(from_user=post.author, to_user=request.user).exists()
    friends = request.user.friends.filter(username=post.author.username).exists()
    comments = post.comments.all()
    comment_form = CommentForm()

    context = {
        'post': post,
        'friend_request_sent': friend_request_sent,
        'friend_request_received': friend_request_received,
        'friends': friends,
        'comments' : comments,
        'comment_form' : comment_form,
    }
    return render(request, 'interior/interior_detail.html', context)


@login_required
def interior_new(request):
    if request.method == "POST":
        form = InteriorPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.furniture_list = '\n'.join(request.POST.getlist('furniture_list[]'))
            post.author = request.user  
            post.save()
            request.user.participation_score += 2
            request.user.save()
            return redirect('interior_user:interior_list')
    else:
        form = InteriorPostForm()
    
    return render(request, 'interior/interior_form.html', {'form': form})

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
    return render(request, 'interior/interior_form.html', {'form': form})

@login_required
def interior_delete(request, pk):
    post = get_object_or_404(InteriorPost, pk=pk)
    if request.user == post.author:
        post.delete()
    return redirect('interior_user:interior_list')

@login_required
def like_interior(request, pk):
    post = get_object_or_404(InteriorPost, pk=pk)

    if isinstance(request.user, AnonymousUser):
        return redirect('users_user:login')
    
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        if post.author is not None:  # post.author가 None이 아닌 경우에만 점수 추가
            post.author.participation_score += 1
            post.author.save()

    return JsonResponse({'liked': liked, 'likes_count': post.total_likes()})

@login_required
def bookmark_interior(request, pk):
    post = get_object_or_404(InteriorPost, pk=pk)

    if isinstance(request.user, AnonymousUser):
        return redirect('users_user:login')
    
    if post.bookmarks.filter(username=request.user.username).exists():
        post.bookmarks.remove(request.user)
        bookmarked = False
    else:
        post.bookmarks.add(request.user)
        bookmarked = True
    return JsonResponse({'bookmarked': bookmarked , 'bookmarks_count':post.total_likes()})


@login_required
def bookmarked_interiors(request):
    user = request.user
    posts = InteriorPost.objects.filter(bookmarks=user).order_by('-date_posted')
    return render(request, 'interior/bookmarked_interiors.html', {'posts': posts})

@require_POST
@login_required
def comments_create(request, pk):
    post = get_object_or_404(InteriorPost, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('interior_user:interior_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'interior/interior_detail.html', {'form': form, 'post': post})


@require_POST
@login_required
def comments_delete(request, pk, id):
    comment = get_object_or_404(InteriorComment, id=id)
    if request.user == comment.user:
        comment.delete()
    return redirect('interior_user:interior_detail', pk=pk)

