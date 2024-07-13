from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
'''
path('create_recipe/', login_required(create_recipe_view), name='create_recipe'),
path('recipe_list/', recipe_list_view, name='recipe_list'),
path('recipe/<int:pk>/', recipe_detail_view, name='recipe_detail'),
path('edit_recipe/', login_required(edit_recipe_view), name='edit_recipe'),
path('delete_recipe/', login_required(delete_recipe_view), name='delete_recipe'),
'''
def create_recipe(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')
        cooking_time = request.POST.get('cooking_time')
        
        if title and ingredients and instructions and cooking_time:
            new_recipe = Recipe(
                title=title,
                ingredients=ingredients,
                instructions=instructions,
                cooking_time=cooking_time
            )
            new_recipe.save()
            return redirect('recipe_detail', pk=new_recipe.pk)
        else:
            # 필요한 인자가 제공되지 않았을 때의 처리
            return redirect('recipe_list')  # 또는 에러 메시지와 함께 폼을 다시 보여줄 수 있습니다
    
    return render(request, 'recipe/create_recipe.html')

            
    