# /order/urls.py

from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    # 재헌
    path('order_list/', views.order_list, name='order_list'),
    path('reservation_list/', views.reservation_list, name='reservation_list'),
    # 재헌끝
]