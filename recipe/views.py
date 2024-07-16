from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe/recipe_list.html', {'recipes': recipes})

def recipe_detail_view(request, id):  # 변경
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
