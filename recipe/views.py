from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Comment
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import RecipeForm, CommentForm

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe/recipe_list.html', {'recipes': recipes})


def recipe_detail_view(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    comments = recipe.comments.all()
    comment_form = CommentForm()
    instructions_with_index = [
        (index + 1, instruction)
        for index, instruction in enumerate(recipe.instructions.splitlines())
    ]
    context = {
        'recipe': recipe,
        'instructions_with_index': instructions_with_index,
        'comments' : comments,
        'comment_form' : comment_form,
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
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.ingredients = '\n'.join(request.POST.getlist('ingredients[]'))
            recipe.instructions = '\n'.join(request.POST.getlist('instructions[]'))
            recipe.save()
            return redirect('recipe_user:recipe_detail', id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
        initial_ingredients = recipe.ingredients.split('\n')
        initial_instructions = recipe.instructions.split('\n')
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
        recipe.delete()
        return redirect('recipe_user:recipe_list')
    else:
        return redirect('recipe_user:recipe_detail', id=recipe.id)  # 변경

@login_required
def like_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if recipe.likes.filter(id=request.user.id).exists():
        recipe.likes.remove(request.user)
    else:
        recipe.likes.add(request.user)
        recipe.author.participation_score += 1
        recipe.author.save()
    return redirect('recipe_user:recipe_detail', id=recipe.id)

@login_required
def bookmark_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.user in recipe.bookmarks.all():
        recipe.bookmarks.remove(request.user)
    else:
        recipe.bookmarks.add(request.user)
    return redirect('recipe_user:recipe_detail', id=recipe.id)

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
        return redirect('recipe_user:recipe_detail', recipe.id)
    return redirect('users_user:login')

@require_POST
def comments_delete(request, recipe_id, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
    return redirect('recipe_user:recipe_detail', recipe_id)