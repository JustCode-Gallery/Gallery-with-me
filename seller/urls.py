# /seller/urls.py

from django.urls import path
from . import views

app_name = 'seller'
urlpatterns = [
    path('seller_reserve/', views.seller_reserve, name='seller_reserve'),
    path('seller_noreserve/', views.seller_noreserve, name='seller_noreserve'),
    path('reserve_cancel/<int:pk>/', views.reserve_cancel, name='reserve_cancel'),
    path('sales/', views.sales_history, name='sales_history'),
    path('settlement_receipt/', views.settlement_receipt, name='settlement_receipt'),
    path('update_account_info/', views.update_account_info, name='update_account_info'),
    path('', views.ArtistListView.as_view(), name='artist_list'),
    path('<int:pk>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('info/', views.seller_info, name='seller_info'),
    path('save_info/', views.save_seller_info, name='save_seller_info'),
    path('upload_image/', views.UploadImageView.as_view(), name='upload_image'),
]