from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from order.models import OrderItem, OrderStatus
from payment.models import Settlement, Commission, SettlementStatus
from user.models import Seller

@shared_task
def update_order_status_and_create_settlement():
    order_complete_status = OrderStatus.objects.get(status='주문 완료')
    order_confirm_status = OrderStatus.objects.get(status='구매 확정')
    settlement_pending_status = SettlementStatus.objects.get(status='정산 전')
    five_minutes_ago = timezone.now() - timedelta(minutes=5) # 테스트를 위해 5분으로 설정

    # 1주일 지난 주문을 '구매 확정'으로 변경
    orders_to_update = OrderItem.objects.filter(order_status=order_complete_status, updated_at__lt=five_minutes_ago)
    for order in orders_to_update:
        order.order_status = order_confirm_status
        order.save()

        # 판매자의 계좌 정보 확인
        seller = order.art_work.seller
        set_account = seller.account if seller.account else None
        set_bank = seller.bank if seller.bank else None
        set_bank_user = seller.bank_user if seller.bank_user else None

        # 정산 테이블 생성
        commission = Commission.objects.first()
        Settlement.objects.create(
            settlement_amount=order.price,
            set_account=set_account,
            set_bank=set_bank,
            set_bank_user=set_bank_user,
            commission=commission.commission,
            vat=commission.vat,
            settlement_status=settlement_pending_status,
            seller=seller,
            order_item=order
        )

@shared_task
def update_settlement_status():
    settlement_status_completed = SettlementStatus.objects.get(status='정산 완료')
    settlements = Settlement.objects.filter(settlement_status__status='정산 전', set_account__isnull=False, set_bank__isnull=False, set_bank_user__isnull=False)

    for settlement in settlements:
        settlement.settlement_status = settlement_status_completed
        settlement.updated_date = timezone.now()
        settlement.save()
