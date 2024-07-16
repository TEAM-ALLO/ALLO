from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import recipe_create_view, recipe_list, recipe_detail_view , recipe_edit_view, recipe_delete_view, bookmarked_recipes, bookmark_recipe, like_recipe, liked_recipes
from django.conf import settings
from django.conf.urls.static import static


app_name = 'recipe_user'

urlpatterns = [
    path('recipe_create/', login_required(recipe_create_view), name='recipe_create'),
    path('recipe_list/', recipe_list, name='recipe_list'),
    path('recipe/<int:id>/', recipe_detail_view ,name='recipe_detail'),
    path('recipe/<int:id>/edit/', login_required(recipe_edit_view), name='recipe_edit'),
    path('recipe/<int:id>/delete/', login_required(recipe_delete_view), name='recipe_delete'),
    path('recipe/<int:id>/like/', like_recipe, name='like_recipe'),
    path('recipe/liked/', liked_recipes, name='liked_recipes'),
    path('recipe/<int:id>/bookmark/', bookmark_recipe, name='bookmark_recipe'),
    path('recipe/bookmarked/', bookmarked_recipes, name='bookmarked_recipes'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)