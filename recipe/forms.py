from django import forms
from .models import Recipe, Comment

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_name', 'cooking_time', 'servings', 'difficulty', 'image']

    ingredients = forms.CharField(widget=forms.HiddenInput(), required=False)
    instructions = forms.CharField(widget=forms.HiddenInput(), required=False)



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']