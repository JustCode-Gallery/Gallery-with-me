import uuid
import os
import requests
import logging
import traceback
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse
from payment.models import Payment, PaymentStatus
from .models import OrderItem, OrderStatus
from artwork.models import ArtWork
from user.models import User
from user.models import ShippingAddress
from django.conf import settings
from dotenv import load_dotenv
import json

load_dotenv()

# 로거 설정
logger = logging.getLogger(__name__)

# 아임포트 API 키 및 시크릿 설정
IMP_API_KEY = os.getenv('PORTONE_PUBLIC_KEY')
IMP_API_SECRET = os.getenv('PORTONE_SECRET_KEY')
KAKAO_CHANNEL_KEY = os.getenv('KAKAO_CHANNEL_KEY')  # 카카오페이 채널 키
TOSS_CHANNEL_KEY = os.getenv('TOSS_CHANNEL_KEY')  # 토스페이 채널 키
KCP_CHANNEL_KEY = os.getenv('KCP_CHANNEL_KEY')  # NHN KCP 채널 키
CUSTOMER_UID = os.getenv('PORTONE_CUSTOMER_UID')

# 토큰 발급
def get_import_token():
    url = "https://api.iamport.kr/users/getToken"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "imp_key": IMP_API_KEY,
        "imp_secret": IMP_API_SECRET
    }
    response = requests.post(url, json=data, headers=headers)
    result = response.json()
    if response.ok:
        return result['response']['access_token']
    else:
        logger.error(f"Failed to get access token: {result}")
        raise Exception('토큰 발급 실패')

# 주문 생성
def create_order(request, artwork_id):
    artwork = get_object_or_404(ArtWork, id=artwork_id)
    user = request.user

    # 결제 상태 "결제 전"을 가져옴
    payment_status = PaymentStatus.objects.get(status='결제 전')

    # Payment 객체 생성
    payment = Payment.objects.create(
        payment_uuid=str(uuid.uuid4()),
        pay_method='Import',
        pay_amount=artwork.price,
        user=user,
        payment_status=payment_status
    )

    # 주문 상태 "주문 대기"를 가져옴
    order_status = OrderStatus.objects.get(status='주문 대기')

    # 기본 배송지 가져오기
    try:
        default_address = ShippingAddress.objects.get(user=user, is_default=True, is_deleted=False)
    except ShippingAddress.DoesNotExist:
        default_address = None

    # OrderItem 객체 생성
    OrderItem.objects.create(
        price=artwork.price,
        art_work=artwork,
        user=user,
        payment=payment,
        order_status=order_status,
        address=default_address  # 기본 배송지 설정
    )

    # 주문 페이지로 리다이렉트
    return redirect('order:order_detail', payment.id)

# 주문 상세
def order_detail(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    order_items = OrderItem.objects.filter(payment=payment)
    regular_order_items = order_items.filter(art_work__is_reservable=False)
    reservable_order_items = order_items.filter(art_work__is_reservable=True)
    return render(request, 'order/order_detail.html', {
        'payment': payment,
        'regular_order_items': regular_order_items,
        'reservable_order_items': reservable_order_items
    })

# 결제 요청
@csrf_exempt
def import_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    order_items = OrderItem.objects.filter(payment=payment)
    user = request.user

    total_price = payment.pay_amount
    orderName = ", ".join([item.art_work.title for item in OrderItem.objects.filter(payment=payment)])
    quantity = OrderItem.objects.filter(payment=payment).count()

    # 결제 승인 URL 생성
    approval_url = request.build_absolute_uri(reverse('order:import_payment_approval'))

    # 아임포트 결제 요청
    context = {
        'payment': payment,
        'orderName': orderName,
        'total_price': total_price,
        'quantity': quantity,
        'imp_api_key': CUSTOMER_UID,
        'kakao_channel_key': KAKAO_CHANNEL_KEY,
        'toss_channel_key': TOSS_CHANNEL_KEY,
        'kcp_channel_key': KCP_CHANNEL_KEY,
        'approval_url': approval_url,
        'order_items': order_items  # OrderItem 추가
    }
    return render(request, 'order/import_payment.html', context)

# 결제 승인 처리
@csrf_exempt
def import_payment_approval(request):
    imp_uid = request.POST.get('imp_uid')
    payment_id = request.POST.get('payment_id')
    payment = get_object_or_404(Payment, id=payment_id)

    # 아임포트 토큰 발급
    try:
        token = get_import_token()
    except Exception as e:
        logger.error(f"Error getting import token: {str(e)}")
        return render(request, 'order/order_fail.html', {'error': '토큰 발급 실패'})

    # 결제 승인 요청
    try:
        url = f"https://api.iamport.kr/payments/{imp_uid}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        result = response.json()

        # 응답 출력 (디버깅용)
        print(result)
        logger.info(f"Import Payment Approval Response: {result}")

        if result.get('response') and result['response'].get('status') == 'paid':
            payment.payment_status = PaymentStatus.objects.get(status='결제 완료')
            payment.pay_date = timezone.now()
            payment.save()

            # 주문 상태를 "주문 완료"로 업데이트
            order_status = OrderStatus.objects.get(status='주문 완료')
            OrderItem.objects.filter(payment=payment).update(order_status=order_status)

            return JsonResponse({'redirect_url': reverse('order:order_success', args=[payment.id])})
        else:
            error_msg = result.get('message', '결제 실패')
            return render(request, 'order/order_fail.html', {'error': error_msg})
    except Exception as e:
        logger.error(f"Error processing payment approval: {str(e)}")
        logger.error(traceback.format_exc())
        return render(request, 'order/order_fail.html', {'error': '결제 승인 처리 중 오류 발생'})

# 결제 성공
def order_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    order_items = OrderItem.objects.filter(payment=payment)
    return render(request, 'order/order_success.html', {'payment': payment, 'order_items': order_items})

# 결제 실패
def order_fail(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    order_item = OrderItem.objects.filter(payment=payment).first()
    artwork_id = order_item.art_work.id if order_item else None
    return render(request, 'order/order_fail.html', {'payment': payment, 'artwork_id': artwork_id, 'error': request.GET.get('error')})

def remove_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    payment_id = item.payment.id
    if item.user == request.user:
        item.delete()
        # Payment 객체의 pay_amount 업데이트
        payment = get_object_or_404(Payment, id=payment_id)
        total_amount = OrderItem.objects.filter(payment=payment).aggregate(Sum('price'))['price__sum']
        payment.pay_amount = total_amount if total_amount is not None else 0
        payment.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'pay_amount': payment.pay_amount, 'item_id': item_id})
        return redirect('order:order_detail', payment_id)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    return redirect('order:order_detail', payment_id)

def order_change_address(request, payment_id):
    address_list = ShippingAddress.objects.filter(user_id=request.user.id, is_deleted=False)
    payment = get_object_or_404(Payment, id=payment_id)
    order_item = OrderItem.objects.filter(payment=payment).first()
    current_address = order_item.address if order_item else None
    return render(request, 'order/order_change_address.html', {
        'address_list': address_list,
        'payment_id': payment_id,
        'current_address': current_address
    })

def create_address(request):
    payment_id = request.POST.get('payment_id')
    if request.method == 'POST':
        if ShippingAddress.objects.filter(user=request.user, is_deleted=False).count() < 5:
            recipient = request.POST.get('recipient')
            phone_number = request.POST.get('phone_number')
            destination = request.POST.get('destination') if request.POST.get('destination') else None
            postal_code = request.POST.get('postal_code')
            address = request.POST.get('address')

            if request.POST.get('extra_address'):
                more_address = request.POST.get('more_address')
                extra_address = request.POST.get('extra_address')
                detail_address = more_address + extra_address
            else:
                detail_address =  request.POST.get('more_address')

            default = request.POST.get('is_default')
            if default:
                ShippingAddress.objects.filter(user=request.user, is_default=True).update(is_default=False)
                is_default = True
            else:
                is_default = False
            user = request.user

            shipping_address = ShippingAddress.objects.create(
                recipient = recipient,
                phone_number = phone_number,
                destination = destination,
                postal_code = postal_code,
                address = address,
                detail_address = detail_address,
                is_default = bool(is_default),
                user = user
            )
            shipping_address.save()
            return redirect('order:order_change_address', payment_id)
        else: 
            address_list = ShippingAddress.objects.filter(user_id=request.user.id, is_deleted=False)
            context = {
                'address_list': address_list,
                'error': '배송지 항목은 최대 5개까지 등록할 수 있습니다.',
                'payment_id': request.POST.get('payment_id')
            }
            return render(request, 'order/order_change_address.html', context)

def delete_address(request, pk):
    address = get_object_or_404(ShippingAddress, pk=pk)
    address.is_deleted = True
    address.save()
    payment_id = request.POST.get('payment_id')
    return redirect('order:order_change_address', payment_id=payment_id)

def update_address(request, pk):
    payment_id = request.POST.get('payment_id')
    address = get_object_or_404(ShippingAddress, pk=pk)
    if request.method == 'POST':
        address.recipient = request.POST.get('recipient', address.recipient)
        address.phone_number = request.POST.get('phone_number', address.phone_number)
        address.destination = request.POST.get('destination', address.destination) if request.POST.get('destination') else None
        address.postal_code = request.POST.get('postal_code', address.postal_code)
        address.address = request.POST.get('address', address.address)

        if request.POST.get('extra_address'):
            more_address = request.POST.get('more_address')
            extra_address = request.POST.get('extra_address')
            address.detail_address = more_address + extra_address
        else:
            address.detail_address =  request.POST.get('more_address')

        is_default = request.POST.get('is_default')
        if is_default:
            ShippingAddress.objects.filter(user=request.user, is_default=True).update(is_default=False)
            address.is_default = True
        else:
            address.is_default = False

        address.save()
        return redirect('order:order_change_address', payment_id)


@csrf_exempt
def set_order_address(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        payment_id = data.get('payment_id')
        address_id = data.get('address_id')

        if not payment_id or not address_id:
            return JsonResponse({'success': False, 'error': 'Missing payment_id or address_id'})

        try:
            address = ShippingAddress.objects.get(id=address_id)
            OrderItem.objects.filter(payment_id=payment_id).update(address=address)
            return JsonResponse({'success': True})
        except ShippingAddress.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid address ID'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def get_address(request, payment_id):
    try:
        order_item = OrderItem.objects.filter(payment_id=payment_id).first()
        if order_item and order_item.address:
            address = order_item.address
            address_info = {
                'recipient': address.recipient,
                'address': address.address,
                'detail_address': address.detail_address,
                'phone_number': address.phone_number,
            }
            return JsonResponse({'success': True, 'address': address_info})
        else:
            return JsonResponse({'success': False, 'error': 'Address not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
def check_address(request, payment_id):
    try:
        order_item = OrderItem.objects.filter(payment_id=payment_id).first()
        if order_item and order_item.address:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Address not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
def check_order_items(request):
    payment_id = request.POST.get('payment_id')
    order_items = OrderItem.objects.filter(payment_id=payment_id)
    
    if not order_items.exists():
        return JsonResponse({'success': False, 'message': '구매할 작품이 없습니다.'})
    
    return JsonResponse({'success': True})