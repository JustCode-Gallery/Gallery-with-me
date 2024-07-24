# /board/urls.py

from django.urls import path
from . import views 

app_name = 'board'
urlpatterns = [
    path('', views.board_list, name='board_list'),
    path('create/', views.board_create, name='board_create'),
    path('create/form/', views.board_create_form, name='board_create_form'),
    path('form_submit/', views.form_submit, name='form_submit'),
    path('detail/<int:pk>/', views.board_detail, name='board_detail'),
    path('temp-upload/', views.temp_upload, name='temp_upload'),
    path('refresh_session/', views.refresh_session, name='refresh_session'),
    path('detail/<int:pk>/edit/', views.board_detail_edit, name='board_detail_edit'),
    path('delete/<int:pk>/', views.board_delete, name='board_delete'),
    path('update/<int:pk>/', views.board_update, name='board_update'),
    path('board_search/', views.board_search, name='board_search'),
    path('exhibit-autocomplete/', views.exhibit_autocomplete, name='exhibit-autocomplete'),

]