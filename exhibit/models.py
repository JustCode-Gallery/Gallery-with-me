from django.db import models

class ArtExhibit(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    address = models.CharField(max_length=100)
    # latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    # longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    department = models.ForeignKey('user.Department', on_delete=models.PROTECT, related_name='exhibit_departments')  # 문자열 기반 참조

class ArtExhibitPoster(models.Model):
    poster_url = models.ImageField() # !이미지필드 경로추가
    exhibit = models.ForeignKey(ArtExhibit, on_delete=models.CASCADE, related_name='images')

class ExhibitBookmark(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)  # 문자열 기반 참조
    exhibit = models.ForeignKey(ArtExhibit, on_delete=models.CASCADE)
