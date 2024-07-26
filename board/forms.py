# board/forms.py
from django import forms
from .models import Post
from exhibit.models import ArtExhibit


class PostForm(forms.ModelForm):
    exhibit_id = forms.ModelChoiceField(
        queryset=ArtExhibit.objects.all(),
        widget=forms.HiddenInput(),  # 실제 ID를 숨겨진 필드로 처리
        required=False
    )
    
    exhibit = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'exhibit', 'placeholder': '전시 입력...'}),  # 사용자에게 보이는 필드
        
    )

    class Meta:
        model = Post
        # 실제 저장받는 필드
        fields = ['post_title', 'post_content', 'exhibit_id']
        widgets = {
            'post_title': forms.TextInput(attrs={'placeholder': '포스트 제목...'}),
            'post_content': forms.Textarea(attrs={'placeholder': '내용 입력...'}),
            # 사용자에게 보이는 필드
            'exhibit': forms.TextInput(attrs={'id': 'exhibit', 'placeholder': '전시 입력...'}),
            # 'exhibit': forms.Select(attrs={'class': 'form-select'}),
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

        
        