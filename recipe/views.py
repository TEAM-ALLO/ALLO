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
        category = self.request.GET.get('category', 'all')
        search_query = self.request.GET.get('search', '')

        if category == 'all':
            queryset = Recipe.objects.all().order_by('-created_at')

        else:
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
        context['preferred_recipes'] = get_user_preferred_recipes_from_csv(self.request)

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
    file_path = os.path.join(settings.BASE_DIR, 'TB_RECIPE_SEARCH-20231130.csv')
    df = pd.read_csv(file_path, header=None, encoding='cp949')
    recipe_names = df[0].tolist()
    return recipe_names

from difflib import SequenceMatcher

def calculate_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_similar_recipes_in_csv(recipe_name, top_n=3, threshold=0.5):
    recipe_names = load_recipe_names_from_csv()
    
    # 유사도 계산
    similar_names = [(name, calculate_similarity(recipe_name, name)) for name in recipe_names]
    
    # 유사도가 threshold 이상인 항목 필터링 및 정렬
    similar_names = [name for name, similarity in sorted(similar_names, key=lambda x: x[1], reverse=True) if similarity >= threshold]
    
    # 중복된 이름 제거
    unique_similar_names = list(dict.fromkeys(similar_names))
    
    return unique_similar_names[:top_n]

import datetime

def get_user_preferred_recipes_from_csv(request, top_n=3):
    try:
        user = request.user  # 현재 사용자를 가져옴
    except AttributeError as e:
        print(f"Error retrieving user: {e}")
        raise
    # 세션에서 추천 목록을 가져옵니다.
    session_key = 'preferred_recipe_list'
    last_update_key = 'last_update'

    # 세션에서 저장된 목록과 마지막 업데이트 날짜를 가져옵니다.
    preferred_recipes = request.session.get(session_key)
    last_update = request.session.get(last_update_key)

    # 현재 날짜 확인
    today = datetime.date.today()

    if preferred_recipes is not None and last_update == str(today):
        # 이미 오늘 업데이트된 목록이 있으면 이를 반환합니다.
        return preferred_recipes
    else:
        # 새 목록을 생성하고 세션에 저장합니다.
        recipe_names = load_recipe_names_from_csv()

        disliked_recipes = UserChoice.objects.filter(user=user, liked=False).values_list('recipe_name', flat=True)
        filtered_recipe_names = [name for name in recipe_names if name not in disliked_recipes]

        if len(filtered_recipe_names) >= top_n:
            preferred_recipe_names = random.sample(filtered_recipe_names, top_n)
        else:
            preferred_recipe_names = filtered_recipe_names

        preferred_recipes = list(Recipe.objects.filter(recipe_name__in=preferred_recipe_names))
        missing_recipe_names = [name for name in preferred_recipe_names if name not in [recipe.recipe_name for recipe in preferred_recipes]]

        preferred_recipes += missing_recipe_names

        # 세션에 저장
        request.session[session_key] = preferred_recipes
        request.session[last_update_key] = str(today)

        return preferred_recipes



@login_required
def recommend_like_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    user_choice, created = UserChoice.objects.get_or_create(user=request.user, recipe=recipe)
    user_choice.liked = True
    user_choice.save()
    return redirect(request.META.get('HTTP_REFERER', 'recipe_user:recipe_list'))

@login_required
def recommend_dislike_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    user_choice, created = UserChoice.objects.get_or_create(user=request.user, recipe=recipe)
    user_choice.liked = False
    user_choice.save()
    return redirect(request.META.get('HTTP_REFERER', 'recipe_user:recipe_list'))


@login_required
def like_csv_recipe(request):
    recipe_name = request.POST.get('recipe_name')
    if recipe_name:
        UserChoice.objects.update_or_create(
            user=request.user, 
            recipe_name=recipe_name,
            defaults={'liked': True}
        )
    return redirect(request.META.get('HTTP_REFERER', 'recipe_user:recipe_list'))

@login_required
def dislike_csv_recipe(request):
    recipe_name = request.POST.get('recipe_name')
    if recipe_name:
        UserChoice.objects.update_or_create(
            user=request.user, 
            recipe_name=recipe_name,
            defaults={'liked': False}
        )
    return redirect(request.META.get('HTTP_REFERER', 'recipe_user:recipe_list'))


def recommend_similar_recipes(request, id):
    selected_recipe = get_object_or_404(Recipe, id=id)
    
    # 데이터베이스에서 비슷한 레시피 찾기 (자신의 게시글 제외)
    similar_recipes_db = get_similar_recipes_based_on_names(selected_recipe.recipe_name, request.user)
    
    # CSV 파일에서 비슷한 레시피 이름 찾기
    similar_recipe_names_csv = find_similar_recipes_in_csv(selected_recipe.recipe_name)
    print(f"Similar recipes in CSV: {similar_recipe_names_csv}")
    
    # CSV 파일에서 찾은 레시피 이름으로 데이터베이스에서 검색
    csv_similar_recipes_db = Recipe.objects.filter(recipe_name__in=similar_recipe_names_csv).exclude(author=request.user)

    # CSV에서 찾은 레시피 이름 중 데이터베이스에 없는 경우 단순 문자열로 추가
    found_names = [recipe.recipe_name for recipe in csv_similar_recipes_db]
    missing_names = [name for name in similar_recipe_names_csv if name not in found_names]

    # **여기서 수정: request.user 대신 request 전달**
    preferred_recipes = get_user_preferred_recipes_from_csv(request)

    if request.method == 'POST':
        selected_recipe_id = request.POST.get('selected_recipe')
        if selected_recipe_id:
            selected_recipe = Recipe.objects.get(id=selected_recipe_id)
            UserChoice.objects.create(user=request.user, recipe=selected_recipe, liked=True)
        else:
            for recipe in similar_recipes_db:
                UserChoice.objects.create(user=request.user, recipe=recipe, liked=False)
            for recipe in csv_similar_recipes_db:
                UserChoice.objects.create(user=request.user, recipe=recipe, liked=False)
        return redirect('recipe_user:recipe_list')

    context = {
        'similar_recipes_db': similar_recipes_db,  # 데이터베이스에서 찾은 레시피
        'csv_similar_recipes_db': csv_similar_recipes_db,  # CSV에서 찾은 레시피 중 데이터베이스에 있는 것
        'missing_names': missing_names,  # CSV에서 찾았지만 데이터베이스에 없는 레시피 이름
        'preferred_recipes': preferred_recipes,
    }
    return render(request, 'recipe/recommendation.html', context)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_levenshtein_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def remove_whitespace(text):
    return text.replace(" ", "")

def get_similar_recipes_based_on_names(recipe_name, user, top_n=5, similarity_threshold=0.1):
    disliked_recipes = UserChoice.objects.filter(user=user, liked=False).values_list('recipe_id', flat=True)
    
    all_recipes = Recipe.objects.exclude(author=user).exclude(id__in=disliked_recipes)
    
    # 띄어쓰기 제거
    recipe_name_no_space = remove_whitespace(recipe_name)
    recipe_names = [remove_whitespace(recipe.recipe_name) for recipe in all_recipes]
    recipe_names.insert(0, recipe_name_no_space)  # 검색어를 첫 번째 위치에 추가
    
    # 각 레시피에 대해 종합 유사도를 계산
    combined_similarities = [get_combined_similarity_score(recipe_name_no_space, name) for name in recipe_names]
    
    # 유사도가 임계값 이상인 레시피 선택
    similar_indices = [i for i, similarity in enumerate(combined_similarities) if similarity >= similarity_threshold]
    
     # 현재 선택된 레시피 이름을 제외하고 상위 top_n 개 추출
    similar_indices = [i for i in similar_indices if recipe_names[i] != recipe_name_no_space][:top_n]
    
    similar_recipes = [all_recipes[i-1] for i in similar_indices]  # i-1로 수정해 all_recipes에서 올바른 인덱스를 가져옵니다.
    
    return similar_recipes




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

    try:
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
    except Exception as e:
        print(f"Error during similarity calculation: {e}")
        return []


@login_required
def recipe_list_view(request):
    preferred_recipes = get_user_preferred_recipes_from_csv(request, top_n=3)  # request를 전달합니다.
    
    context = {
        'preferred_recipes': preferred_recipes,
        # 다른 필요한 컨텍스트
    }
    return render(request, 'recipe/recipe_list.html', context)

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['preferred_recipes'] = get_user_preferred_recipes_from_csv(self.request)  # self.request를 전달합니다.
    return context

def calculate_word_based_similarity(recipe_name_1, recipe_name_2):
    words_1 = set(recipe_name_1.split())
    words_2 = set(recipe_name_2.split())
    
    intersection = words_1.intersection(words_2)
    union = words_1.union(words_2)
    
    return len(intersection) / len(union)

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

def calculate_cosine_similarity(recipe_name_1, recipe_name_2):
    vectorizer = TfidfVectorizer()  # 또는 다른 적절한 벡터라이저 사용
    tfidf_matrix = vectorizer.fit_transform([recipe_name_1, recipe_name_2])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]


def get_embedding_based_similarity(recipe_name_1, recipe_name_2):
    embedding_1 = model.encode(recipe_name_1)
    embedding_2 = model.encode(recipe_name_2)
    return cosine_similarity([embedding_1], [embedding_2])[0][0]

def get_combined_similarity_score(recipe_name_1, recipe_name_2):
    cos_sim = calculate_cosine_similarity(recipe_name_1, recipe_name_2)
    lev_sim = calculate_levenshtein_similarity(recipe_name_1, recipe_name_2)
    word_sim = calculate_word_based_similarity(recipe_name_1, recipe_name_2)
    embed_sim = get_embedding_based_similarity(recipe_name_1, recipe_name_2)
    
    # 각 유사도에 가중치를 부여하여 결합
    return (cos_sim + lev_sim + word_sim + embed_sim) / 4

