from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='photos/')
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=15)
    created_at = models.DateField()
    email = models.EmailField(unique=True)  # 이메일 중복 불가 설정
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # related_name 변경
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name=('groups'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # related_name 변경
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )

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
    art_work = models.ForeignKey('artwork.ArtWork', on_delete=models.CASCADE)  # 문자열 기반 참조

class University(models.Model):
    name = models.CharField(max_length=255)
    email_domain = models.CharField(max_length=255)

class Department(models.Model):
    name = models.CharField(max_length=20)
    exhibit = models.ForeignKey('exhibit.ArtExhibit', on_delete=models.CASCADE, related_name='department_exhibits')  # 문자열 기반 참조
    university = models.ForeignKey(University, on_delete=models.CASCADE)

class Seller(User):
    bank = models.CharField(max_length=20)
    bank_user = models.CharField(max_length=20)
    account = models.CharField(max_length=20)  # 계좌번호는 문자열로 처리
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
