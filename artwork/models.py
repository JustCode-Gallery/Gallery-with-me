from django.db import models
from user.models import User, Seller
from exhibit.models import ArtExhibit

class ArtWork(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    width = models.IntegerField()
    height = models.IntegerField()
    depth = models.IntegerField()
    created_at = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 금액은 DecimalField로 처리
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    exhibit = models.ForeignKey(ArtExhibit, on_delete=models.CASCADE)

class ArtImage(models.Model):
    image_url = models.URLField()
    artwork = models.ForeignKey(ArtWork, on_delete=models.CASCADE)

class Material(models.Model):
    name = models.CharField(max_length=50)

class ArtWorkMaterial(models.Model):
    art_work = models.ForeignKey(ArtWork, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

class WorkLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    art_work = models.ForeignKey(ArtWork, on_delete=models.CASCADE)

class TagCategory(models.Model):
    name = models.CharField(max_length=50)

class Tag(models.Model):
    name = models.CharField(max_length=50)
    tag_category = models.ForeignKey(TagCategory, on_delete=models.CASCADE)

class ArtTag(models.Model):
    art_work = models.ForeignKey(ArtWork, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

class ArtistInquiry(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField()
    completed_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
