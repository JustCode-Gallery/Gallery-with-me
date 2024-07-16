from django import forms
from .models import Tag, TagCategory, Material, ArtistInquiry

class ArtWorkFilterForm(forms.Form):
    Material_tag_search = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='재료'
    )

    # 태그 검색 필드 추가
    def __init__(self, *args, **kwargs):
        super(ArtWorkFilterForm, self).__init__(*args, **kwargs)
        tag_categories = TagCategory.objects.all()
        for category in tag_categories:
            self.fields[category.name] = forms.ModelMultipleChoiceField(
                queryset=Tag.objects.filter(tag_category=category),
                required=False,
                widget=forms.CheckboxSelectMultiple,
                label=category.name,
            )

    def label_from_instance(self, obj): # 모델 인스턴스 name 속성을 가져오기
        return obj.name

class ArtistInquiryForm(forms.ModelForm):
    class Meta:
        model = ArtistInquiry
        fields = ['question']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        labels = {
            'question': '문의 내용',
        }

class ArtWorkSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)