from django import forms
from .models import InteriorPost, InteriorComment

class InteriorPostForm(forms.ModelForm):
    class Meta:
        model = InteriorPost
        fields = ['title', 'content', 'image', 'category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = InteriorComment
        fields = ['content']