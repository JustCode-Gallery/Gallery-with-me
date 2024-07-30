from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ShippingAddress, UserPreferArt, University, Department, University_Department, Seller

# 사용자 정의 UserAdmin
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'nickname', 'photo_url', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'phone_number', 'destination', 'postal_code', 'address', 'is_default', 'user', 'is_deleted')
    search_fields = ('recipient', 'phone_number', 'destination', 'postal_code', 'address')
    list_filter = ('is_default', 'is_deleted')

class UserPreferArtAdmin(admin.ModelAdmin):
    list_display = ('user', 'art_work', 'created_at')
    search_fields = ('user__username', 'art_work__title')
    list_filter = ('created_at',)

class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'email_domain')
    search_fields = ('name',)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class UniversityDepartmentAdmin(admin.ModelAdmin):
    list_display = ('university', 'department')
    search_fields = ('university__name', 'department__name')
    list_filter = ('university', 'department')

class SellerAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'nickname', 'photo_url', 'phone_number', 'bank', 'bank_user', 'account', 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'bank', 'bank_user', 'account', 'department')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'bank', 'bank_user', 'account')
    ordering = ('username',)

# 등록
admin.site.register(User, UserAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(UserPreferArt, UserPreferArtAdmin)
admin.site.register(University, UniversityAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(University_Department, UniversityDepartmentAdmin)
admin.site.register(Seller, SellerAdmin)
