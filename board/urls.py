# /board/urls.py

from django.urls import path
from .views import board_list, board_detail, board_create, board_create_form
app_name = 'board'
urlpatterns = [
    path('', board_list, name='board_list'),
    path('create/', board_create, name='board_create'),
    path('create/form/', board_create_form, name='board_create_form'),
    path('detail/', board_detail, name='board_detail'),


]