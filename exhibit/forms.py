from django import forms
from .models import ArtExhibit, ArtExhibitPoster
from user.models import Department
from django.forms import inlineformset_factory, BaseInlineFormSet

class ArtExhibitForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    
    class Meta:
        model = ArtExhibit
        fields = ['title', 'description', 'start_date', 'end_date', 'address', 'latitude', 'longitude', 'department']

class ArtExhibitPosterForm(forms.ModelForm):
    class Meta:
        model = ArtExhibitPoster
        fields = ['poster_url']  # 포스터 URL 필드만 포함
