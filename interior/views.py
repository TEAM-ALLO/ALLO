from django.shortcuts import render, get_object_or_404, redirect
from .models import InteriorPost, InteriorComment
from community.models import FriendRequest
from .forms import InteriorPostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse


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
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'interior/interior_detail.html', context)


@login_required
def interior_new(request):
    if request.method == "POST":
        form = InteriorPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.furniture_list = request.POST.get('furniture_list', '')
            post.author = request.user  
            post.save()
            request.user.participation_score += 2
            request.user.save()
            return redirect('interior_user:interior_detail', pk=post.pk)
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
            return redirect('interior_user:interior_detail',pk=post.pk)
    else:
        form = InteriorPostForm(instance=post)
    return render(request, 'interior/interior_form.html', {'form': form})

@login_required
def interior_delete(request, pk):
    post = get_object_or_404(InteriorPost, pk=pk)
    if request.user == post.author:
        request.user.participation_score -= 2  # 참여 점수 감소
        request.user.save()
        post.delete()
    return redirect('interior_user:interior_list')

@login_required
def like_interior(request, pk):
    post = get_object_or_404(InteriorPost, pk=pk)

    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request type'})

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

    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request type'})

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
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        request.user.participation_score += 1
        request.user.save()

        comments = post.comments.all().values('id', 'user__username', 'content', 'created_at')
        comments_list = list(comments)
    
        return JsonResponse({
            'success': True,
            'comments': comments_list,
            'total_comments': post.comments.count()  # 댓글 총 개수를 반환
        })
    else:
        return JsonResponse({'success': False, 'errors': comment_form.errors})

@require_POST
@login_required
def comments_delete(request, pk, id):
    post = get_object_or_404(InteriorPost, pk=pk)
    comment = get_object_or_404(InteriorComment, id=id)
    if request.user == comment.user:
        request.user.participation_score -= 1  # 참여 점수 감소
        request.user.save()
        comment.delete()

        comments = post.comments.all().values('id', 'user__username', 'content', 'created_at')
        comments_list = list(comments)

        return JsonResponse({
            'success': True,
            'comments': comments_list,
            'total_comments': post.comments.count()  # 댓글 총 개수를 반환
        })
    else:
        return JsonResponse({'success': False, 'message': 'Unauthorized'})
