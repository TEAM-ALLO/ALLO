from django import forms
from .models import Recipe, Comment

class RecipeForm(forms.ModelForm):
    category = forms.ChoiceField(choices=Recipe.CATEGORY_CHOICES, required=True, label="카테고리")

    class Meta:
        model = Recipe
        fields = ['recipe_name', 'cooking_time', 'servings', 'difficulty', 'image', 'category']
        
    ingredients = forms.CharField(widget=forms.HiddenInput(), required=False)
    instructions = forms.CharField(widget=forms.HiddenInput(), required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
