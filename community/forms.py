from django import forms
from .models import CommunityPost, Message, Comment, Event

class PostForm(forms.ModelForm):
    class Meta:
        model = CommunityPost
        fields = ['title', 'content','image']

class MessageForm(forms.ModelForm):
    content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': '메시지를 입력하세요...'}),
    )

    class Meta:
        model = Message
        fields = ['content', 'image']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        image = cleaned_data.get('image')

        if not content and not image:
            raise forms.ValidationError("내용이나 이미지를 입력해야 합니다.")

        return cleaned_data

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


