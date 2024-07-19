from django import forms
from .models import InteriorPost

class InteriorPostForm(forms.ModelForm):
    class Meta:
        model = InteriorPost
        fields = ['title', 'content', 'image', 'category']
