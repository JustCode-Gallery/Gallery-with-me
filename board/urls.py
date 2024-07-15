# /board/urls.py

from django.urls import path
from .views import board_list, board_detail, board_create, board_create_form, temp_upload, form_submit

app_name = 'board'
urlpatterns = [
    path('', board_list, name='board_list'),
    path('create/', board_create, name='board_create'),
    path('create/form/', board_create_form, name='board_create_form'),
    path('form_submit/', form_submit, name='form_submit'),
    path('detail/', board_detail, name='board_detail'),
    # path('detail/<int:pk>/', board_detail, name='board_detail'),
    path('temp-upload/', temp_upload, name='temp_upload'),


]