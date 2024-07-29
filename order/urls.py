from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    # 재헌
    path('order_list/', views.order_list, name='order_list'),
    path('reservation_list/', views.reservation_list, name='reservation_list'),
    # 재헌끝
    path('create_order/<int:artwork_id>/', views.create_order, name='create_order'),
    path('order_detail/<int:payment_id>/', views.order_detail, name='order_detail'),
    path('import_payment/<int:payment_id>/', views.import_payment, name='import_payment'),
    path('import_payment_approval/', views.import_payment_approval, name='import_payment_approval'),
    path('order_success/<int:payment_id>/', views.order_success, name='order_success'),
    path('order_fail/<int:payment_id>/', views.order_fail, name='order_fail'),
    path('remove_item/<int:item_id>/', views.remove_item, name='remove_item'),
    path('order_change_address/<int:payment_id>/', views.order_change_address, name='order_change_address'),
    path('order_change_address/create/', views.create_address, name='create_address'),
    path('order_change_address/delete/<int:pk>/', views.delete_address, name='delete_address'),
    path('order_change_address/update/<int:pk>/', views.update_address, name='update_address'),
    path('set_order_address/', views.set_order_address, name='set_order_address'),
    path('get_address/<int:payment_id>/', views.get_address, name='get_address'),
    path('check_address/<int:payment_id>/', views.check_address, name='check_address'),
    path('check_order_items/', views.check_order_items, name='check_order_items'),
    path('cart/', views.cart_list, name='cart'),
    path('delete_cart_item/<int:cart_id>/', views.delete_cart_item, name='delete_cart_item'),
]