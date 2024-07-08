from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # 기본 사용자 모델에는 username, password, email, first_name, last_name 등 기본적인 필드들이 포함.
    # username은 식별자
    nickname = models.CharField(max_length=50)
    photo_url = models.URLField(null=True)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
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
    art_work = models.ForeignKey('artwork.ArtWork', on_delete=models.CASCADE)

class University(models.Model):
    name = models.CharField(max_length=50)
    email_domain = models.CharField(max_length=50, null=True)

class Department(models.Model):
    name = models.CharField(max_length=20)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

class Seller(User):
    bank = models.CharField(max_length=20)
    bank_user = models.CharField(max_length=20)
    account = models.CharField(max_length=20)  # 계좌번호는 문자열로 처리
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
