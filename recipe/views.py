from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Comment
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import RecipeForm, CommentForm
from django.views.generic import ListView
from django.db.models import Q
from community.models import FriendRequest
from django.http import JsonResponse

class RecipeListView(ListView):
    model = Recipe  # 사용할 모델 지정
    paginate_by = 6  # 페이지당 항목 수
    template_name = 'recipe/recipe_list.html'  # 사용할 템플릿
    context_object_name = 'recipes'  # 템플릿에서 사용할 컨텍스트 변수 이름

    def get_queryset(self):
        # 기본적으로 모든 레시피를 ID의 역순으로 정렬하여 가져옴
        queryset = Recipe.objects.order_by('-id')

        # GET 요청에서 카테고리와 검색어를 가져옴
        category = self.request.GET.get('category', '')
        search_query = self.request.GET.get('search', '')

        # 카테고리가 존재하면 해당 카테고리의 레시피만 필터링
        if category:
            queryset = queryset.filter(category=category)
        # 검색어가 1자보다 길면 레시피 이름과 작성자 이름에서 검색어가 포함된 레시피를 필터링
        if search_query and len(search_query) > 1:
            queryset = queryset.filter(
                Q(recipe_name__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )

        return queryset  # 필터링된 레시피 목록 반환

    def get_context_data(self, **kwargs):
        # 기본 컨텍스트 데이터를 가져옴
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']  # 페이지네이터 객체 가져오기
        page_numbers_range = 5  # 페이지네이션 범위 설정
        max_index = len(paginator.page_range)  # 페이지 범위의 최대 인덱스 가져오기
        page = self.request.GET.get('page')  # 현재 페이지 번호 가져오기
        current_page = int(page) if page else 1  # 현재 페이지 번호 설정 (기본값은 1)
        # 페이지네이션 범위 계산
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]  # 페이지네이션 범위 설정
        context['page_range'] = page_range  # 페이지네이션 범위를 컨텍스트에 추가

        category = self.request.GET.get('category', '')  # 카테고리 가져오기
        search_query = self.request.GET.get('search', '')  # 검색어 가져오기

        # 카테고리가 존재하면 해당 카테고리 이름을 컨텍스트에 추가, 그렇지 않으면 '레시피'로 설정
        if category:
            context['category_name'] = dict(Recipe.CATEGORY_CHOICES).get(category, '레시피')
        else:
            context['category_name'] = '레시피'

        context['search_query'] = search_query  # 검색어를 컨텍스트에 추가

        # 가장 인기 있는 레시피를 좋아요 수를 기준으로 가져오기
        popular_recipe = self.get_queryset().order_by('-likes').first()
        context['popular_recipe'] = popular_recipe  # 인기 레시피를 컨텍스트에 추가

        return context  # 최종 컨텍스트 반환

# 기존 recipe_list 뷰는 삭제합니다.



def recipe_detail_view(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    comments = recipe.comments.all()
    comment_form = CommentForm()
    friend_request_sent = FriendRequest.objects.filter(from_user=request.user, to_user=recipe.author).exists()
    friend_request_received = FriendRequest.objects.filter(from_user=recipe.author, to_user=request.user).exists()
    instructions_with_index = [
        (index + 1, instruction)
        for index, instruction in enumerate(recipe.instructions.splitlines())
    ]
    context = {
        'recipe': recipe,
        'instructions_with_index': instructions_with_index,
        'comments' : comments,
        'comment_form' : comment_form,
        'friend_request_sent': friend_request_sent,
        'friend_request_received': friend_request_received,
    }
    return render(request, 'recipe/recipe_detail.html', context)

@login_required
def recipe_create_view(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.ingredients = '\n'.join(request.POST.getlist('ingredients[]'))
            recipe.instructions = '\n'.join(request.POST.getlist('instructions[]'))
            recipe.save()
            request.user.participation_score += 2
            request.user.save()
            return redirect('recipe_user:recipe_detail', id=recipe.id)
    else:
        form = RecipeForm()
    return render(request, 'recipe/recipe_form.html', {'form': form})

@login_required
def recipe_edit_view(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.user != recipe.author:
        return redirect('recipe_user:recipe_detail', id=recipe.id)
    
    initial_ingredients = recipe.ingredients.split('\n') if recipe.ingredients else []
    initial_instructions = recipe.instructions.split('\n') if recipe.instructions else []
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.ingredients = '\n'.join(request.POST.getlist('ingredients[]'))
            recipe.instructions = '\n'.join(request.POST.getlist('instructions[]'))
            recipe.save()
            return redirect('recipe_user:recipe_detail', id=recipe.id)
        else: 
            print('땡')
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipe/recipe_edit.html', {
        'form': form, 
        'recipe': recipe,
        'initial_ingredients': initial_ingredients,
        'initial_instructions': initial_instructions
    })

@login_required
def recipe_delete_view(request, id):  # 변경
    recipe = get_object_or_404(Recipe, id=id)  # 변경
    if request.user == recipe.author:
        request.user.participation_score -= 2  # 참여 점수 감소
        request.user.save()
        recipe.delete()
        return redirect('recipe_user:recipe_list')
    else:
        return redirect('recipe_user:recipe_detail', id=recipe.id)  # 변경

@login_required
@require_POST
def like_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if recipe.likes.filter(username=request.user.username).exists():
        recipe.likes.remove(request.user)
    else:
        recipe.likes.add(request.user)
        recipe.author.participation_score += 1
        recipe.author.save()
    return JsonResponse({'liked': recipe.likes.filter(username=request.user.username).exists(), 'likes_count': recipe.likes.count()})

@login_required
@require_POST
def bookmark_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if recipe.bookmarks.filter(username=request.user.username).exists():
        recipe.bookmarks.remove(request.user)
    else:
        recipe.bookmarks.add(request.user)
    return JsonResponse({'bookmarked': recipe.bookmarks.filter(username=request.user.username).exists(), 'bookmarks_count': recipe.bookmarks.count()})


@login_required
def liked_recipes(request):
    user = request.user
    recipes = Recipe.objects.filter(likes=user).order_by('-date_posted')
    return render(request, 'recipe/recipe_liked.html', {'recipes': recipes})

@login_required
def bookmarked_recipes(request):
    user = request.user
    recipes = Recipe.objects.filter(bookmarks=user).order_by('-date_posted')
    return render(request, 'recipe/recipe_bookmarked.html', {'recipes': recipes})

@require_POST
def comments_create(request, id):
    if request.user.is_authenticated:
        recipe = get_object_or_404(Recipe, id=id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            comment.save()
            request.user.participation_score += 1
            request.user.save()
        return redirect('recipe_user:recipe_detail', recipe.id)
    return redirect('users_user:login')

@require_POST
def comments_delete(request, recipe_id, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            request.user.participation_score -= 1  # 참여 점수 감소
            request.user.save()
            comment.delete()
    return redirect('recipe_user:recipe_detail', recipe_id)