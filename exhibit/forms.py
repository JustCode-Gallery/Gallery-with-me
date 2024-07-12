from django import forms
from .models import ArtExhibit

class ArtExhibitForm(forms.ModelForm):
    class Meta:
        model = ArtExhibit
        fields = ['title', 'description', 'start_date', 'end_date', 'address', 'latitude', 'longitude']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
