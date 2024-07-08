from django.contrib.auth.models import AbstractUser
from django.db import models
from artwork.models import ArtWork
from exhibit.models import ArtExhibit

class User(AbstractUser):
    # 기본 사용자 모델에는 username, password, email, first_name, last_name 등 기본적인 필드들이 포함.
    # username은 식별자
    nickname = models.CharField(max_length=50)
    photo_url = models.URLField(null=True)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    email = models.EmailField(unique=True)

class Seller(User):
    bank = models.CharField(max_length=20)
    bank_user = models.CharField(max_length=20)
    account = models.CharField(max_length=20)  # 계좌번호는 문자열로 처리
    department = models.ForeignKey('Department')

class ShippingAddress(models.Model):
    recipient = models.CharField(max_length=20, null=True)
    phone_number = models.CharField(max_length=15)
    destination = models.CharField(max_length=50, null=True)
    postal_code = models.CharField(max_length=5)
    address = models.CharField(max_length=50)
    detail_address = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class UserPreferArt(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    art_work = models.ForeignKey(ArtWork, on_delete=models.CASCADE)

class University(models.Model):
    name = models.CharField(max_length=50)
    email_domain = models.CharField(max_length=50, null=True)

class Department(models.Model):
    name = models.CharField(max_length=20)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
