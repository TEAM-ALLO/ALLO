from django import forms
from .models import Recycle

class RecycleForm(forms.ModelForm):
    class Meta:
        model = Recycle
        fields = ['category', 'name', 'description', 'image', 'tip']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

class NewField (forms.ModelForm):
    class Meta:
        model = Recycle
        fields = ['category', 'name', 'description', 'image', 'tip']