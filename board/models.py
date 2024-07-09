from django.db import models

class Post(models.Model):
    post_title = models.CharField(max_length=255)
    post_content = models.TextField()
    post_timestamp = models.DateTimeField()
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)  # 문자열 기반 참조
    exhibit = models.ForeignKey('exhibit.ArtExhibit', on_delete=models.CASCADE)  # 문자열 기반 참조

class PostImage(models.Model):
    image_url = models.ImageField(upload_to='post_images/')
    image_order = models.IntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

# class PostComment(models.Model):
#     comment_content = models.TextField()
#     comment_timestamp = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey('user.User', on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
