from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe/recipe_list.html', {'recipes': recipes})


def recipe_detail(request, id):  # 변경
    recipe = get_object_or_404(Recipe, id=id)  # 변경
    return render(request, 'recipe/recipe_detail.html', {'recipe': recipe})


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
