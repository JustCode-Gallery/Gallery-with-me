from django.db import models
from user.models import User

class ArtExhibit(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    address = models.CharField(max_length=50)

class ArtExhibitPoster(models.Model):
    poster = models.ImageField(upload_to='posters/')
    exhibit = models.ForeignKey(ArtExhibit, on_delete=models.CASCADE)

class ExhibitBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exhibit = models.ForeignKey(ArtExhibit, on_delete=models.CASCADE)
