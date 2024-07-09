# /artwork/urls.py
from django.urls import path
from . import views

app_name = 'artwork'
urlpatterns = [
    path('artwork_list/', views.ArtWorkListView.as_view(), name='artwork_list'),
    path('artwork/<int:pk>/', views.ArtWorkDetailView.as_view(), name='artwork_detail'),
    path('artwork/<int:pk>/like/', views.toggle_work_like, name='toggle_work_like'),
    path('artwork/<int:pk>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('artwork/<int:pk>/buy_now/', views.buy_now, name='buy_now'),
    path('artwork/<int:pk>/add_inquiry/', views.add_inquiry, name='add_inquiry'),
    path('artwork/<int:pk>/reserve/', views.reserve_artwork, name='reserve_artwork'),
    path('load_more_artworks/', views.load_more_artworks, name='load_more_artworks'),
]