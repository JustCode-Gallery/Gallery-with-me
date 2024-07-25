from django.shortcuts import render
# 재헌
from order.models import OrderItem,OrderStatus,Reservation
# 재헌끝

# Create your views here.

# 재헌
def order_list(request):
    orders=OrderItem.objects.filter(user=request.user)
    return render(request,'order/order_list.html',{'orders':orders})

def reservation_list(request):
    reservations=Reservation.objects.filter(user=request.user)
    return render(request,'order/order_list.html',{'reservations':reservations})

# 재헌끝