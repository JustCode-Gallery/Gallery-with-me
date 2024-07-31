# exhibit/serializers.py

from rest_framework import serializers
from .models import ArtExhibit, ArtExhibitPoster

class ArtExhibitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtExhibit
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'address', 'latitude', 'longitude', 'department']

class ArtExhibitPosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtExhibitPoster
        fields = ['id', 'poster_url']
