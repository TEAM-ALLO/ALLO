from django.shortcuts import render, get_object_or_404, redirect
from .models import InteriorPost, InteriorComment
from community.models import FriendRequest
from .forms import InteriorPostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.contenttypes.models import ContentType
from users.models import Notification
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
import random
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def interior_list(request):
    category = request.GET.get('category', 'all')
    query = request.GET.get('q', '')

    if category == 'all':
        posts = InteriorPost.objects.all().order_by('-created_at')
    else:
        posts = InteriorPost.objects.filter(category=category).order_by('-created_at')
    
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    # 최근 일주일 동안의 인기글 계산
    one_week_ago = timezone.now() - timedelta(days=7)
    recent_posts = InteriorPost.objects.filter(created_at__gte=one_week_ago)

    # 하트 수가 1개 이상인 게시글 중에서 인기글을 선택
    popular_posts = [post for post in recent_posts if post.total_likes() > 0]
    if popular_posts:
        max_engagement = max(post.total_engagements() for post in popular_posts)
        top_posts = [post for post in popular_posts if post.total_engagements() == max_engagement]
        popular_post = random.choice(top_posts) if top_posts else None
    else:
        popular_post = None

    # 페이지네이션 설정
    paginator = Paginator(posts, 9)  # 페이지당 9개의 게시글
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer, show the first page
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # If page_number is out of range, show the last page
        page_obj = paginator.get_page(paginator.num_pages)

    page_range = paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)

    context = {
        'posts': page_obj,
        'category': category,
        'query': query,
        'popular_post': popular_post if not query else None,  # 검색어가 있을 때는 인기글 숨김
        'page_obj': page_obj,
        'page_range': page_range,
        'category_name': '기타' if category == 'others' else category,  # 카테고리 이름 설정
        'no_results': not page_obj.object_list.exists(),
    }

    return render(request, 'interior/interior_list.html', context)


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
        'furniture_list': post.furniture_list.split(',') if post.furniture_list else [],  # split the list for display
    }
    return render(request, 'interior/interior_detail.html', context)



@login_required
def interior_new(request):
    if request.method == "POST":
        form = InteriorPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            furniture_list = request.POST.getlist('furniture_list[]')
            # 빈 값 제거
            furniture_list = [item for item in furniture_list if item.strip()]
            post.furniture_list = ','.join(furniture_list)
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
        form = InteriorPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            furniture_list = request.POST.getlist('furniture_list[]')
            # 빈 값 제거
            furniture_list = [item for item in furniture_list if item.strip()]
            post.furniture_list = ','.join(furniture_list)
            post.save()
            return redirect('interior_user:interior_detail', pk=post.pk)
    else:
        form = InteriorPostForm(instance=post)
        furniture_list = post.furniture_list.split(',') if post.furniture_list else []

    return render(request, 'interior/interior_form.html', {'form': form, 'furniture_list': furniture_list})


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
        if post.author is not None:
            post.author.participation_score += 1
            post.author.save()

            # 알림 생성
            Notification.objects.create(
                user=post.author,
                sender=request.user,
                notification_type='like',
                content_type=ContentType.objects.get_for_model(post),
                object_id=post.pk
            )

    return JsonResponse({'liked': liked, 'likes_count': post.total_likes()})

@login_required
def bookmark_interior(request, pk):
    post = get_object_or_404(InteriorPost, pk=pk)

    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request type'})

    if post.bookmarks.filter(pk=request.user.pk).exists():
        post.bookmarks.remove(request.user)
        bookmarked = False
    else:
        post.bookmarks.add(request.user)
        bookmarked = True
        
    return JsonResponse({'success': True, 'bookmarked': bookmarked, 'bookmarks_count': post.total_bookmarks()})

@login_required
def bookmarked_interiors(request):
    user = request.user
    posts = InteriorPost.objects.filter(bookmarks=user).order_by('-date_posted')
    return render(request, 'interior/bookmarked_interiors.html', {'posts': posts})

@receiver(post_save, sender=InteriorComment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.post.author,  # 댓글이 달린 게시글의 작성자에게 알림
            sender=instance.user,  # 댓글을 단 사용자
            notification_type='comment',
            content_type=ContentType.objects.get_for_model(instance.post),
            object_id=instance.post.pk
        )

@require_POST
@login_required
def comments_create(request, pk):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post_id = pk
        comment.user = request.user
        comment.save()
        request.user.participation_score += 1
        request.user.save()
        comments = InteriorComment.objects.filter(post_id=pk).values('id', 'user__username', 'content')
        comments_list = comments.count()
    
        return JsonResponse({
            'success': True,
            'comments': list(comments),
            'total_comments': comments_list  # 댓글 총 개수를 반환
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
