# board/forms.py
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_title', 'post_content', 'exhibit']
        widgets = {
            'post_title': forms.TextInput(attrs={'placeholder': '포스트 제목...'}),
            'post_content': forms.Textarea(attrs={'placeholder': '내용 입력...'}),
            'exhibit': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'post_title': '',  
            'post_content': '',
            'exhibit':'전시',
        }
        
        