from django.db import models
from user.models import User, Department

class ArtExhibit(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    address = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.PROTECT) # SET_NULL?

class ArtExhibitPoster(models.Model):
    poster_url = models.URLField()
    exhibit = models.ForeignKey(ArtExhibit, on_delete=models.CASCADE, related_name='images')

class ExhibitBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exhibit = models.ForeignKey(ArtExhibit, on_delete=models.CASCADE)
