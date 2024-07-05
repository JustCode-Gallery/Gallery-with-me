from django.db import models
from user.models import User, Seller
from order.models import OrderItem

class PaymentStatus(models.Model):
    status = models.CharField(max_length=10)

class Payment(models.Model):
    payment_uuid = models.CharField(max_length=50)
    pay_method = models.CharField(max_length=20)
    pay_date = models.DateTimeField()
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2)  # 금액은 DecimalField로 처리
    pay_nobank_user = models.CharField(max_length=20)
    pay_nobank = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE)

class SettlementStatus(models.Model):
    status = models.CharField(max_length=10)

class Settlement(models.Model):
    settlement_date = models.DateTimeField()
    updated_date = models.DateTimeField()
    settlement_amount = models.DecimalField(max_digits=10, decimal_places=2)  # 금액은 DecimalField로 처리
    set_account = models.CharField(max_length=20)  # 계좌번호는 문자열로 처리
    set_bank = models.CharField(max_length=20)  # 은행 이름은 문자열로 처리
    set_bank_user = models.CharField(max_length=20)
    commission = models.DecimalField(max_digits=10, decimal_places=2)  # 금액은 DecimalField로 처리
    vat = models.DecimalField(max_digits=10, decimal_places=2)  # 금액은 DecimalField로 처리
    settlement_status = models.ForeignKey(SettlementStatus, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)


class Commission(models.Model):
    commission = models.DecimalField(max_digits=10, decimal_places=2)  # 금액은 DecimalField로 처리
    vat = models.DecimalField(max_digits=10, decimal_places=2)  # 금액은 DecimalField로 처리
