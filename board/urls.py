# /board/urls.py

from django.urls import path
from .views import board_list

app_name = 'board'
urlpatterns = [
    path('', board_list, name='board_list'),
]