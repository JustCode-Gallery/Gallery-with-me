# /order/urls.py

from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
     path('cart/', views.cart_list, name='cart'),
     path('delete_cart_item/<int:cart_id>/', views.delete_cart_item, name='delete_cart_item'),
]