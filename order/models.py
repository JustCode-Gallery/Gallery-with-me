from django.db import models
from user.models import User
from artwork.models import ArtWork
from payment.models import Payment

class OrderStatus(models.Model):
    status = models.CharField(max_length=10)

class OrderItem(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 금액은 DecimalField로 처리
    art_work = models.ForeignKey(ArtWork, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)

class RefundRequest(models.Model):
    reason = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)

class RefundImg(models.Model):
    img = models.ImageField(upload_to='refund_images/')
    refund_request = models.ForeignKey(RefundRequest, on_delete=models.CASCADE)

class Reservation(models.Model):
    created_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    art_work = models.ForeignKey(ArtWork, on_delete=models.CASCADE)

class Cart(models.Model):
    cart_created_at = models.DateTimeField()
    is_direct = models.BooleanField()
    art_work = models.ForeignKey(ArtWork, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
