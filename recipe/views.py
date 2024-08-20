from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Comment, UserChoice
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import RecipeForm, CommentForm
from django.views.generic import ListView
from community.models import FriendRequest
from django.http import JsonResponse
from users.models import Notification
from django.contrib.contenttypes.models import ContentType
import random
import pandas as pd
import os
from django.conf import settings

class RecipeListView(ListView):
    model = Recipe
    paginate_by = 6
    template_name = 'recipe/recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        queryset = Recipe.objects.order_by('-id')
        category = self.request.GET.get('category', '')
        search_query = self.request.GET.get('search', '')

        if category:
            queryset = queryset.filter(category=category)

        if search_query:
            queryset = queryset.filter(recipe_name__icontains=search_query)


        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        category = self.request.GET.get('category', '')
        search_query = self.request.GET.get('search', '')

        if category:
            context['category_name'] = dict(Recipe.CATEGORY_CHOICES).get(category, '레시피')
        else:
            context['category_name'] = '레시피'

        context['search_query'] = search_query
        context['no_results'] = search_query and not context['recipes']

        # 개인적인 취향에 맞춘 추천 레시피 추가
        context['preferred_recipes'] = get_user_preferred_recipes_from_csv(self.request.user)

        popular_recipe = self.get_queryset().order_by('-likes').first()
        context['popular_recipe'] = popular_recipe

        return context

@login_required
def recipe_detail_view(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    comments = recipe.comments.all()
    comment_form = CommentForm()
    friend_request_sent = FriendRequest.objects.filter(from_user=request.user, to_user=recipe.author).exists()
    friend_request_received = FriendRequest.objects.filter(from_user=recipe.author, to_user=request.user).exists()
    friends = request.user.friends.filter(username=recipe.author.username).exists()
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
        'friends':friends,
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
        
        # 좋아요 알림 생성
        if recipe.author != request.user:  # 본인에게는 알림이 가지 않도록
            Notification.objects.create(
                user=recipe.author,
                sender=request.user,
                notification_type='like',
                content_type=ContentType.objects.get_for_model(recipe),
                object_id=recipe.id
            )
    
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
@login_required
def comments_create(request, id):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.recipe_id = id
        comment.user = request.user
        comment.save()
        request.user.participation_score += 1
        request.user.save()

        # 댓글 알림 생성
        recipe = comment.recipe
        if recipe.author != request.user:  # 본인에게는 알림이 가지 않도록
            Notification.objects.create(
                user=recipe.author,
                sender=request.user,
                notification_type='comment',
                content_type=ContentType.objects.get_for_model(recipe),
                object_id=recipe.id
            )

        comments = Comment.objects.filter(recipe_id=id).values('id', 'user__username', 'content')
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
def comments_delete(request, recipe_id, comment_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        request.user.participation_score -= 1  # 참여 점수 감소
        request.user.save()
        comment.delete()

        comments = recipe.comments.all().values('id', 'user__username', 'content', 'created_at')
        comments_list = list(comments)

        return JsonResponse({
            'success': True,
            'comments': comments_list,
            'total_comments': recipe.comments.count()  # 댓글 총 개수를 반환
        }, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'success': False, 'message': 'Unauthorized'})


def get_similar_recipes(recipe_id, top_n=3):
    if count_matrix is None or df is None:
        return []

    cosine_sim = cosine_similarity(count_matrix)
    idx = df.index[df['id'] == recipe_id].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n + 1]

    similar_recipes = [df.iloc[i[0]]['id'] for i in sim_scores]
    return Recipe.objects.filter(id__in=similar_recipes)

def load_recipe_names_from_csv():
    # CSV 파일 경로 설정
    file_path_1 = os.path.join(settings.BASE_DIR, 'TB_RECIPE_SEARCH-220701.csv')
    file_path_2 = os.path.join(settings.BASE_DIR, 'TB_RECIPE_SEARCH-20231130.csv')

    # CSV 파일 로드
    with open(file_path_1, 'r', encoding='cp949', errors='replace') as f1:
        df1 = pd.read_csv(f1)
    with open(file_path_2, 'r', encoding='cp949', errors='replace') as f2:
        df2 = pd.read_csv(f2)

    # C열에 해당하는 요리 이름 추출
    recipe_names_1 = df1.iloc[:, 2].dropna().unique()  # C열 (0-index라서 2)
    recipe_names_2 = df2.iloc[:, 2].dropna().unique()

    # 두 파일의 요리 이름 합치기
    recipe_names = list(set(recipe_names_1).union(set(recipe_names_2)))

    return recipe_names



def get_user_preferred_recipes_from_csv(user, top_n=3):
    # CSV에서 레시피 이름을 가져옵니다.
    recipe_names = load_recipe_names_from_csv()

    # 무작위로 top_n개의 레시피 이름을 선택합니다.
    preferred_recipe_names = random.sample(recipe_names, top_n)

    # 해당 레시피 이름에 해당하는 Recipe 인스턴스를 반환합니다.
    preferred_recipes = Recipe.objects.filter(recipe_name__in=preferred_recipe_names)
    return preferred_recipes

@login_required
def recommend_similar_recipes(request, id):
    selected_recipe = get_object_or_404(Recipe, id=id)
    similar_recipes = get_similar_recipes_based_on_names(selected_recipe.recipe_name, request.user)
    preferred_recipes = get_user_preferred_recipes_from_csv(request.user)

    if request.method == 'POST':
        selected_recipe_id = request.POST.get('selected_recipe')
        if selected_recipe_id:
            selected_recipe = Recipe.objects.get(id=selected_recipe_id)
            UserChoice.objects.create(user=request.user, recipe=selected_recipe, liked=True)
        else:
            for recipe in similar_recipes:
                UserChoice.objects.create(user=request.user, recipe=recipe, liked=False)
            for recipe in preferred_recipes:
                UserChoice.objects.create(user=request.user, recipe=recipe, liked=False)
        return redirect('recipe_user:recipe_list')


    context = {
        'similar_recipes': similar_recipes,
        'preferred_recipes': preferred_recipes,
    }
    return render(request, 'recipe/recommendation.html', context)


def get_similar_recipes_based_on_names(recipe_name, user, top_n=3):
    disliked_recipes = UserChoice.objects.filter(user=user, liked=False).values_list('recipe_id', flat=True)
    print(f"Disliked recipes for user {user.username}: {list(disliked_recipes)}")
    
    recipes = Recipe.objects.filter(recipe_name__icontains=recipe_name).exclude(id__in=disliked_recipes).order_by('?')[:top_n]
    print(f"Found {recipes.count()} similar recipes for recipe name '{recipe_name}'")
    
    return recipes

import os
import pickle
from django.conf import settings
from sklearn.metrics.pairwise import cosine_similarity

vectorizer_path = os.path.join(settings.BASE_DIR, 'count_vectorizer.pkl')
df_path = os.path.join(settings.BASE_DIR, 'recipes_df.pkl')

if os.path.exists(vectorizer_path) and os.path.exists(df_path):
    with open(vectorizer_path, 'rb') as f:
        count_matrix = pickle.load(f)
    with open(df_path, 'rb') as f:
        df = pickle.load(f)
else:
    count_matrix = None
    df = None

def get_similar_recipes(recipe_id, top_n=3):
    if count_matrix is None or df is None:
        print("Count matrix or DataFrame is not loaded")
        return []

    cosine_sim = cosine_similarity(count_matrix)
    idx = df.index[df['id'] == recipe_id].tolist()
    if not idx:
        print(f"No index found for recipe ID {recipe_id}")
        return []
    
    idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n + 1]
    
    similar_recipes = [df.iloc[i[0]]['id'] for i in sim_scores]
    print(f"Similar recipes IDs: {similar_recipes}")
    
    return Recipe.objects.filter(id__in=similar_recipes)