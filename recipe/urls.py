from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import recipe_create_view, recipe_list_view,recipe_detail_view, recipe_edit_view, recipe_delete_view
from django.conf import settings
from django.conf.urls.static import static

app_name = "recipe"

urlpatterns = [
    path('recipe_create/', login_required(recipe_create_view), name='recipe_create'),
    path('recipe_list/', recipe_list_view, name='recipe_list'),
    path('recipe/<int:id>/', recipe_detail_view, name='recipe_detail'),
    path('recipe/<int:id>/edit/', login_required(recipe_edit_view), name='recipe_edit'),
    path('recipe/<int:id>/delete/', login_required(recipe_delete_view), name='recipe_delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)