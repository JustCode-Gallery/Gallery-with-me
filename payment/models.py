from django.db import models

class PaymentStatus(models.Model):
    status = models.CharField(max_length=10)

class Payment(models.Model):
    payment_uuid = models.CharField(max_length=50, unique=True, null=True)
    pay_method = models.CharField(max_length=20)  # 카카오페이, 카드, 무통장
    pay_date = models.DateTimeField(null=True)  # 실제 결제가 확인되면(payment_status가 '결제완료'로 바뀔 때) pay_date 필드 업데이트
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_escro_user = models.CharField(max_length=20, null=True)  # 예금주
    pay_escro = models.CharField(max_length=20, null=True)
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)  # 문자열 기반 참조
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.PROTECT)  # PaymentStatus 객체 삭제 시도 시 ProtectError 내서 삭제할 수 없게

    def __str__(self):
        return f"{self.user.name}님의 결제정보" if self.user.id else "{self.payment_uuid}의 결제정보"

class SettlementStatus(models.Model):
    status = models.CharField(max_length=10)

class Settlement(models.Model):
    settlement_date = models.DateTimeField(auto_now_add=True)  # 정산 요청 시 생성
    updated_date = models.DateTimeField(auto_now=True, null=True)  # 정산이 완료되면(settlement_status가 '처리완료'로 바뀔 때) updated_date 필드 업데이트
    settlement_amount = models.DecimalField(max_digits=10, decimal_places=2)
    set_account = models.IntegerField(null=True)  # 계좌번호
    set_bank = models.CharField(max_length=20, null=True)
    set_bank_user = models.CharField(max_length=20, null=True)
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    settlement_status = models.ForeignKey(SettlementStatus, on_delete=models.PROTECT)
    seller = models.ForeignKey('user.Seller', on_delete=models.SET_NULL, null=True)  # 문자열 기반 참조
    order_item = models.ForeignKey('order.OrderItem', on_delete=models.PROTECT)  # 문자열 기반 참조

    def __str__(self):
        return f"{self.seller.name}님의 정산정보" if self.seller.id else f"{self.set_bank} {self.set_account}의 정산정보"

class Commission(models.Model):
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
