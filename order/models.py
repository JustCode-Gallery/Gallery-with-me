from django.db import models
from user.models import User
from artwork.models import ArtWork
from payment.models import Payment

class OrderStatus(models.Model):
    status = models.CharField(max_length=10)

class OrderItem(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 금액은 DecimalField로 처리
    art_work = models.ForeignKey(ArtWork, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)

class RefundRequest(models.Model):
    reason = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)

class RefundImg(models.Model):
    image_url = models.URLField()
    refund_request = models.ForeignKey(RefundRequest, on_delete=models.CASCADE, related_name='images')

class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    art_work = models.ForeignKey(ArtWork, on_delete=models.CASCADE)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    is_direct = models.BooleanField(default=False)
    art_work = models.ForeignKey(ArtWork, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
