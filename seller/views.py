from django.shortcuts import render, redirect
from order.models import Reservation
from artwork.models import ArtWork, ArtImage
from user.models import User,Seller
from order.models import OrderItem, OrderStatus
from payment.models import Settlement, SettlementStatus
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.views import generic

# 판매자 예약
def seller_reserve(request): 
    # 예약 작품 구매예약 조회
    # 예약취소
    # 예약 알림
    # 예약일시 / 예약작품 / 예약중 / 결제금액 / 결제수단 / 예약번호?

    ## 판매자인지 확인 
    user = request.user
    try:
        seller = Seller.objects.get(id=user.id)
    except Seller.DoesNotExist:
            return render(request, 'home.html', {
                'error_message': '등록된 판매자를 찾을 수 없습니다'
            })
    ## 등록한 작품 확인 > 없음 > 없음페이지
    try:
        artwork = ArtWork.objects.get(seller_id=seller.id)
    except ArtWork.DoesNotExist:
        return render(request,'seller/seller_noreserve.html')

    ## 있음 > 예약 작품인지 확인 
    #### 등록작품이 여러개일 경우 >> 추후개발
    if artwork:
        if artwork.is_reservable:
            ## 예약 모델에 예약작품 있는지 확인 
            reservation = Reservation.objects.filter(user=user, art_work=artwork)
            # filter로 가야하는지 > html변경
            artworks_with_images = []
            images = ArtImage.objects.filter(artwork=artwork)
            artworks_with_images.append({
                    'artwork': artwork,
                    'images': images
                })
        ## 예약 작품 아님 
        else:
            return render(request,'seller/seller_noreserve.html')
    
    context = {
        'artworks_with_images': artworks_with_images,
        'reservation': reservation,
    }
    
    return render(request,'seller/seller_reserve.html', context)

def seller_noreserve(request): 
    return render(request,'seller/seller_noreserve')

def reserve_cancel(request,pk): 
    if request.method=="POST":
        reason = request.POST.get('reason')
        # 예약 가져옴
        reservation = Reservation.objects.get(pk=pk)

        # reservation 취소사유 저장 
        reservation.cancel_reason = reason
        reservation.status = False
        reservation.save()
        
        # 주문DB 상태변경 / 작품DB is_sold 변경
                
        orderItem = OrderItem.objects.get(art_work_id = reservation.art_work_id,
                                          order_status_id__lte=2)
        orderItem.order_status_id = 5
        orderItem.save()
        artwork = ArtWork.objects.get(seller_id=reservation.user_id)
        artwork.is_sold = False
        artwork.save()
            
        # 구매자에게 알림 뱃지 / 이메일
        # 시그널
        # 어떻게 유저에게 신호를 뱃지 표시
        # 실시간 반영
        return redirect('seller:seller_reserve')

    return render(request,'seller/seller_reserve.html')

def sales_history(request):
    seller = request.user.seller
    filter_confirmed = request.GET.get('filter') == 'confirmed'
    if filter_confirmed:
        confirmed_status = OrderStatus.objects.get(status='구매 확정')
        sales_list = OrderItem.objects.filter(art_work__seller=seller, order_status=confirmed_status).select_related('art_work', 'order_status').prefetch_related('art_work__artimage_set').order_by('-updated_at')
    else:
        sales_list = OrderItem.objects.filter(art_work__seller=seller).select_related('art_work', 'order_status').prefetch_related('art_work__artimage_set').order_by('-updated_at')

    paginator = Paginator(sales_list, 10)  # 한 페이지에 10개씩
    page = request.GET.get('page')
    sales = paginator.get_page(page)

    context = {
        'sales': sales,
        'filter_confirmed': filter_confirmed,
    }
    return render(request, 'seller/sales_history.html', context)

def settlement_receipt(request):
    seller = request.user.seller
    status_filter = request.GET.get('status', 'pending')  # 기본값은 'pending'
    if status_filter == 'completed':
        settlement_status = SettlementStatus.objects.get(status='정산 완료')
    else:
        settlement_status = SettlementStatus.objects.get(status='정산 전')

    settlements = Settlement.objects.filter(seller=seller, settlement_status=settlement_status).order_by('-settlement_date')
    
    # 정산 금액 계산
    for settlement in settlements:
        commission_amount = settlement.settlement_amount * (settlement.commission / 100)
        vat_amount = commission_amount * (settlement.vat / 100)
        net_amount = settlement.settlement_amount - (commission_amount + vat_amount)
        settlement.net_amount = net_amount

    default_account_info = {
        'set_account': seller.account,
        'set_bank': seller.bank,
        'set_bank_user': seller.bank_user
    }

    context = {
        'settlements': settlements,
        'default_account_info': default_account_info,
        'status_filter': status_filter,
    }
    return render(request, 'seller/settlement_receipt.html', context)

@require_POST
def update_account_info(request):
    seller = request.user.seller
    account_info = request.POST.get('account_info')
    bank = request.POST.get('bank')
    bank_user = request.POST.get('bank_user')

    # 판매자의 계좌 정보 업데이트
    seller.account = account_info
    seller.bank = bank
    seller.bank_user = bank_user
    seller.save()

    # 업데이트 할 정산 테이블 필터링 ('정산 전' 상태)
    settlements = Settlement.objects.filter(seller=seller, settlement_status__status='정산 전')

    # 정보 업데이트
    for settlement in settlements:
        settlement.set_account = account_info
        settlement.set_bank = bank
        settlement.set_bank_user = bank_user
        settlement.save()

    return JsonResponse({'success': True})

def seller_info(request):
    seller = Seller.objects.get(user_ptr_id=request.user.id)
    info = seller.info
    context = {
        'seller': seller,
        'info': info,
    }
    return render(request, 'seller/seller_info.html', context)

def save_seller_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        info = data.get('info')

        seller = Seller.objects.get(user_ptr_id=request.user.id)
        seller.info = info
        seller.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

class ArtistListView(generic.ListView):
    model = Seller
    template_name = 'seller/artist_list.html'
    context_object_name = 'artist_list'

class ArtistDetailView(generic.DetailView):
    model = Seller
    template_name = 'seller/artist_detail.html'
    context_object_name = 'artist'