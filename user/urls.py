# /user/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('update_profile/', views.update_profile, name='update_profile'), 
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
    path('select_register/', views.select_register, name='select_register'),
    path('register/seller/', views.register_seller, name='register_seller'),
    path('update_profile/seller/', views.update_seller_profile, name='update_seller_profile'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    path('delete_account/', views.delete_account, name='delete_account'),
    path('find_password/', views.find_password, name='find_password'),
    path('change_password/', views.change_password, name='change_password'),
    path('select_artworks/', views.select_artworks, name='select_artworks'),
    path('change_address/', views.change_address, name='change_address'),
    path('change_address/create/', views.create_address, name='create_address'),
    path('change_address/delete/<int:pk>/', views.delete_address, name='delete_address'),
    path('change_address/update/<int:pk>/', views.update_address, name='update_address'),

]