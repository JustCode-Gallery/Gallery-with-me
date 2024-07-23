# /exhibit/urls.py

from django.urls import path
from .views import *

app_name = 'exhibit'
urlpatterns = [
    path('', exhibit_list, name='exhibit_list'),
    path('exhibit_detail/<int:exhibit_id>/', exhibit_detail, name='exhibit_detail'),
    path('create/', create_exhibit, name='create_exhibit'),
    path('exhibit_like_list/', exhibit_like_list, name='exhibit_like_list'),

]