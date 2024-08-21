from django import forms
from .models import InteriorPost, InteriorComment

class InteriorPostForm(forms.ModelForm):
    category = forms.ChoiceField(choices=InteriorPost.CATEGORY_CHOICES, required=True, label="카테고리")
    furniture_list = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = InteriorPost
        fields = ['title', 'content', 'image', 'category','furniture_list']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }

        
class CommentForm(forms.ModelForm):
    class Meta:
        model = InteriorComment
        fields = ['content']