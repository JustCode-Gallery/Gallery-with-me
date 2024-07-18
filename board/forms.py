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
            # 'exhibit': forms.Select(attrs={'class': 'form-select'}),
            'exhibit': forms.TextInput(attrs={'placeholder': '전시 입력...'}),
        }
        labels = {
            'post_title': '',  
            'post_content': '',
            'exhibit':'전시',
        }

class PostSearchForm(forms.Form):
    search_word = forms.CharField(
        label= '',
        widget=forms.TextInput(attrs={
            'placeholder': '포스트 검색',
            'id': 'search-query'
            })
    )

        
        