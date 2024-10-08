from django.db import models

class ArtExhibit(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    address = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=25, decimal_places=20, null=True, blank=True)
    longitude = models.DecimalField(max_digits=25, decimal_places=20, null=True, blank=True)
    university_department = models.ForeignKey('user.University_Department', on_delete=models.PROTECT, related_name='exhibit_departments')  # 문자열 기반 참조
    
    def __str__(self):
        return self.title

class ArtExhibitPoster(models.Model):
    poster_url = models.ImageField(upload_to='poster_image/') # !이미지필드 경로추가
    exhibit = models.ForeignKey(ArtExhibit, on_delete=models.CASCADE, related_name='images')

class ExhibitBookmark(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)  # 문자열 기반 참조
    exhibit = models.ForeignKey(ArtExhibit, on_delete=models.CASCADE)
