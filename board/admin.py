from django.contrib import admin
from .models import Post, PostImage

# Register your models here.
class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 3

class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]

admin.site.register(Post, PostAdmin)

