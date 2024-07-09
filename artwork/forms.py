from django import forms
from .models import Tag, TagCategory, Material, ArtistInquiry

class ArtWorkFilterForm(forms.Form):

    최소가격 = forms.IntegerField(required=False, label='최소가격')
    최대가격 = forms.IntegerField(required=False, label='최대가격')
    최소너비 = forms.IntegerField(required=False, label='최소너비')
    최대너비 = forms.IntegerField(required=False, label='최대너비')
    최소높이 = forms.IntegerField(required=False, label='최소높이')
    최대높이 = forms.IntegerField(required=False, label='최대높이')
    재료 = forms.ModelMultipleChoiceField(
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