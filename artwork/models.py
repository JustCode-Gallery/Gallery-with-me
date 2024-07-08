from django.db import models
from user.models import User, Seller
from exhibit.models import ArtExhibit

class ArtWork(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    width = models.IntegerField()
    height = models.IntegerField()
    depth = models.IntegerField()
    created_at = models.DateField(auto_now_add=True) # 생성될 때
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 금액은 DecimalField로 처리
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    exhibit = models.ForeignKey(ArtExhibit, on_delete=models.SET_NULL, null=True) # 전시 삭제시 or 전시 없는 경우, NULL로 설정
    is_sold = models.BooleanField() # 판매 여부 체크

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
    tag_category = models.ForeignKey(TagCategory, on_delete=models.PROTECT) # TagCategory의 하위 Tag가 존재할 경우, 삭제되지 않도록 설정

class ArtTag(models.Model):
    art_work = models.ForeignKey(ArtWork, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

class ArtistInquiry(models.Model):
    question = models.TextField()
    answer = models.TextField(null=True) # 답변은 null 값 허용(이후에 입력되는 필드)
    created_at = models.DateTimeField(auto_now_add=True) # 생성될 때
    completed_at = models.DateTimeField(auto_now=True) # 수정될 때, answer가 올라올 때 시간 설정하기
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True) # seller가 삭제되었을 경우 NULL, User에게는 '판매자 회원 정보가 없습니다.'같은 게시물로 보이도록 하기
