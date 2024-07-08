from django.db import models
from user.models import User
from exhibit.models import ArtExhibit

class Post(models.Model):
    post_title = models.CharField(max_length=255)
    post_content = models.TextField()
    post_timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)         
    exhibit = models.ForeignKey(ArtExhibit, on_delete=models.SET_DEFAULT, default="Deleted_Exhibit")    # 전시 삭제 시 남김

class PostImage(models.Model):
    image_url = models.URLField()
    image_order = models.IntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

# Disqus사용
# class PostComment(models.Model):
#     comment_content = models.TextField()
#     comment_timestamp = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)      
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
