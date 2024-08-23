from django.db import models
from user.models import ShippingAddress

class OrderStatus(models.Model):
    status = models.CharField(max_length=10)

    def __str__(self):
        return self.status

class OrderItem(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 금액은 DecimalField로 처리
    art_work = models.ForeignKey('artwork.ArtWork', on_delete=models.SET_NULL, null=True)  # 문자열 기반 참조
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)  # 문자열 기반 참조
    payment = models.ForeignKey('payment.Payment', on_delete=models.PROTECT)  # 문자열 기반 참조
    order_status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)
    address = models.ForeignKey(ShippingAddress, on_delete=models.PROTECT, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.art_work and self.art_work.is_reservable:
            Reservation.objects.get_or_create(
                user=self.art_work.seller,
                art_work=self.art_work,
                cancel_reason = None
            )

class RefundRequest(models.Model):
    reason = models.CharField(max_length=500)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)  # 문자열 기반 참조
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)

class RefundImg(models.Model):
    image_url = models.ImageField(upload_to='refund_images/') 
    refund_request = models.ForeignKey(RefundRequest, on_delete=models.CASCADE, related_name='images')

class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)  # 문자열 기반 참조
    art_work = models.ForeignKey('artwork.ArtWork', on_delete=models.CASCADE)  # 문자열 기반 참조
    updated_at = models.DateTimeField(auto_now=True)
    cancel_reason = models.CharField(max_length=500, null=True)
    status = models.BooleanField(default=True)
    order = models.ForeignKey(OrderItem, on_delete=models.CASCADE)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    is_direct = models.BooleanField(default=False)
    art_work = models.ForeignKey('artwork.ArtWork', on_delete=models.CASCADE)  # 문자열 기반 참조
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)  # 문자열 기반 참조
