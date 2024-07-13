from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_name', 'cooking_time', 'servings', 'difficulty', 'image']

    ingredients = forms.CharField(widget=forms.HiddenInput(), required=False)
    instructions = forms.CharField(widget=forms.HiddenInput(), required=False)