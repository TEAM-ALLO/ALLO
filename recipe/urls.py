from django.urls import path
from .views import recipe

urlpatterns = [
    path('recipe/', recipe, name='recipe'),
]
