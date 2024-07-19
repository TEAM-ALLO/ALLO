from django import forms
from .models import CommunityPost, Message, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = CommunityPost
        fields = ['title', 'content']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
