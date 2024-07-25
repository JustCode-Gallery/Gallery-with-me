from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('create_order/<int:artwork_id>/', views.create_order, name='create_order'),
    path('order_detail/<int:payment_id>/', views.order_detail, name='order_detail'),
    path('import_payment/<int:payment_id>/', views.import_payment, name='import_payment'),
    path('import_payment_approval/', views.import_payment_approval, name='import_payment_approval'),
    path('order_success/<int:payment_id>/', views.order_success, name='order_success'),
    path('order_fail/<int:payment_id>/', views.order_fail, name='order_fail'),
    path('remove_item/<int:item_id>/', views.remove_item, name='remove_item'),
    path('order_change_address/', views.order_change_address, name='order_change_address'),
    path('order_change_address/create/', views.create_address, name='create_address'),
    path('order_change_address/delete/<int:pk>/', views.delete_address, name='delete_address'),
    path('order_change_address/update/<int:pk>/', views.update_address, name='update_address'),

]