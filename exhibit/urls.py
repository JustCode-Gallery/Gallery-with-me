# /exhibit/urls.py

from django.urls import path
from .views import *

app_name = 'exhibit'
urlpatterns = [
    path('', exhibit_list, name='exhibit_list'),
    path('map/<int:exhibit_id>/', exhibit_map, name='exhibit_map'),
]