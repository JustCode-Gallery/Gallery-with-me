# /artwork/urls.py
from django.urls import path
from . import views

app_name = 'artwork'
urlpatterns = [
    path('artwork_list/', views.ArtWorkListView.as_view(), name='artwork_list'),
    path('api/tag-material-categories/', views.tag_material_categories_api, name='tag_material_categories_api'),
    path('<int:pk>/', views.ArtWorkDetailView.as_view(), name='artwork_detail'),
    path('<int:pk>/like/', views.toggle_work_like, name='toggle_work_like'),
    path('<int:pk>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('<int:pk>/buy_now/', views.buy_now, name='buy_now'),
    path('<int:pk>/add_inquiry/', views.add_inquiry, name='add_inquiry'),
    path('<int:pk>/reserve/', views.reserve_artwork, name='reserve_artwork'),
    path('load_more_artworks/', views.load_more_artworks, name='load_more_artworks'),
    path('create/', views.create_artwork, name='create_artwork'),
    path('update/<int:artwork_id>/', views.update_artwork, name='update_artwork'),
    path('delete/<int:artwork_id>/', views.delete_artwork, name='delete_artwork'),
    path('artwork_list/seller/', views.seller_artwork_list, name='seller_artwork_list'),
    path('artwork_like_list/', views.artwork_like_list, name='artwork_like_list'),
    path('user_inquiry_list/', views.user_inquiry_list, name='user_inquiry_list'),


]