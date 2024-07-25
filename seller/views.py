from django.shortcuts import render, redirect
from order.models import Reservation
from artwork.models import ArtWork, ArtImage
from user.models import User,Seller
# Create your views here.

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
            reservation = Reservation.objects.get(user=user, art_work=artwork)
            
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
    # if request.method=="POST":

        # reason = request.POST.get('reason')

        # # 예약 가져옴
        # reservation = Reservation.object.get(pk=pk)

        # # reservation 취소사유 저장 
        # # updated_at = models.DateTimeField(auto_now_add=True)
        # # cancel_reason = models.CharField(max_length=200)
        # reservation.cancel_reason = reason
        # reservation.save()

        
        # # 예약상태 취소 artwork is_reservable 상태변경
        # artwork = ArtWork.objects.get(id=reservation.art_work_id)
        # artwork.is_reservable = False
        # artwork.save()
            
        # # 구매자에게 알림 뱃지 / 이메일
        # # 시그널
        # # 어떻게 유저에게 신호를 뱃지 표시
        # # 실시간 반영
        # reservation.user_id
        


        # return redirect('seller:seller_reserve')
    
    
        
        

    return render(request,'seller/seller_reserve.html')