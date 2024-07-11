from django import forms
from .models import Tag, TagCategory, Material, ArtistInquiry

class ArtWorkFilterForm(forms.Form):

    min_price = forms.IntegerField(required=False, label='최소가격')
    max_price = forms.IntegerField(required=False, label='최대가격')
    min_width = forms.IntegerField(required=False, label='최소너비')
    max_width = forms.IntegerField(required=False, label='최대너비')
    min_height = forms.IntegerField(required=False, label='최소높이')
    max_height = forms.IntegerField(required=False, label='최대높이')
    Material_tag_search = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='재료'
    )

    def __init__(self, *args, **kwargs):
        super(ArtWorkFilterForm, self).__init__(*args, **kwargs)

        tag_categories = TagCategory.objects.all()
        for category in tag_categories: # 태그 테이블 내의 정보 가져오기
            field_name = category.name
            self.fields[field_name] = forms.ModelMultipleChoiceField(
                queryset=Tag.objects.filter(tag_category=category),
                required=False,
                widget=forms.CheckboxSelectMultiple,
                label=field_name
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