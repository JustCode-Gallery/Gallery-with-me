from django.contrib import admin
from .models import ArtWork, ArtImage, Material, ArtWorkMaterial, WorkLike, TagCategory, Tag, ArtTag, ArtistInquiry

@admin.register(ArtWork)
class ArtWorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'width', 'height', 'depth', 'created_at', 'price', 'is_sold', 'seller', 'exhibit')
    list_filter = ('is_sold', 'created_at', 'seller', 'exhibit')
    search_fields = ('title', 'description', 'seller__name', 'exhibit__title')

@admin.register(ArtImage)
class ArtImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_url', 'artwork')
    search_fields = ('artwork__title',)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(ArtWorkMaterial)
class ArtWorkMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'art_work', 'material')
    search_fields = ('art_work__title', 'material__name')

@admin.register(WorkLike)
class WorkLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'art_work')
    search_fields = ('user__username', 'art_work__title')

@admin.register(TagCategory)
class TagCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tag_category')
    search_fields = ('name', 'tag_category__name')

@admin.register(ArtTag)
class ArtTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'art_work', 'tag')
    search_fields = ('art_work__title', 'tag__name')

@admin.register(ArtistInquiry)
class ArtistInquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'created_at', 'completed_at', 'user', 'seller')
    list_filter = ('created_at', 'completed_at', 'seller')
    search_fields = ('question', 'answer', 'user__username', 'seller__username')
