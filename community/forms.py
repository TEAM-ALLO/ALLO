from django import forms
from .models import CommunityPost, Message, Comment, Event

class PostForm(forms.ModelForm):
    class Meta:
        model = CommunityPost
        fields = ['title', 'content','image']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class EventForm(forms.ModelForm):
    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Event
        fields = ['title', 'start_date', 'end_date', 'description','image']


