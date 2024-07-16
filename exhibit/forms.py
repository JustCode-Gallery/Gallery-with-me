from django import forms
from .models import ArtExhibit
from user.models import Department

class ArtExhibitForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    
    class Meta:
        model = ArtExhibit
        fields = ['title', 'description', 'start_date', 'end_date', 'address', 'latitude', 'longitude', 'department']
