# /board/urls.py

from django.urls import path
from .views import board_list,board_detail,board_create
app_name = 'board'
urlpatterns = [
    path('', board_list, name='board_list'),
    path('create/', board_create, name='board_create'),
    path('detail/', board_detail, name='board_detail'),


]