from django.contrib.auth.models import AbstractUser
from django.db import models
from artwork.models import ArtWork
from exhibit.models import ArtExhibit

class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='photos/')
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=15)
    created_at = models.DateField()
    email = models.EmailField(unique=True)  # 이메일 중복 불가 설정

class ShippingAddress(models.Model):
    recipient = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    destination = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=5)
    address = models.CharField(max_length=50)
    detail_address = models.CharField(max_length=50)
    is_default = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class UserPreferArt(models.Model):
    created_at = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    art_work = models.ForeignKey(ArtWork, on_delete=models.CASCADE)

class University(models.Model):
    name = models.CharField(max_length=255)
    email_domain = models.CharField(max_length=255)

class Department(models.Model):
    name = models.CharField(max_length=20)
    exhibit = models.ForeignKey(ArtExhibit, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

class Seller(User):
    bank = models.CharField(max_length=20)
    bank_user = models.CharField(max_length=20)
    account = models.CharField(max_length=20)  # 계좌번호는 문자열로 처리
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
