# /seller/urls.py

from django.urls import path
from . import views

app_name = 'seller'
urlpatterns = [
    path('seller_reserve/', views.seller_reserve, name='seller_reserve'),
    path('seller_noreserve/', views.seller_noreserve, name='seller_noreserve'),
    path('reserve_cancel/', views.reserve_cancel, name='reserve_cancel'),
]