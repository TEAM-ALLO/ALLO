from django import forms
from .models import CommunityPost

class PostForm(forms.ModelForm):
    class Meta:
        model = CommunityPost
        fields = ['title', 'content']
