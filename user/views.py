from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from user.models import *
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from artwork.models import *
from django.http import JsonResponse
from .utils import generate_verification_code, send_verification_email
import json 
from django.contrib import messages
from order.models import OrderItem, OrderStatus, RefundRequest, RefundImg
from payment.models import Payment, PaymentStatus, SettlementStatus, Settlement
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

def find_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        email_verification_code = request.POST.get('email_verification_code')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # 인증 코드 확인
        if email_verification_code == request.session.get('email_verification_code'):
            try:
                # 사용자 검색
                user = User.objects.get(email=email, first_name=first_name, last_name=last_name, phone_number=phone_number)

                # 비밀번호 확인
                if new_password1 == new_password2:
                    user.set_password(new_password1)  # 비밀번호 암호화
                    user.save()  # 사용자 객체 저장
                    login(request, user)  # 사용자 로그인
                    return redirect('home')
                else:
                    messages.error(request, '새 비밀번호를 다시 입력해주세요.')
                    return render(request, 'find_password.html')

            except User.DoesNotExist:
                messages.error(request, '등록되지 않은 회원입니다.')
                return render(request, 'find_password.html')

        else:
            messages.error(request, '유효하지 않은 인증 코드입니다.')
            return render(request, 'find_password.html')

    return render(request, 'find_password.html')

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        email_verification_code = request.POST['email_verification_code']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        nickname = request.POST['nickname']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        photo = request.FILES.get('photo')

        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        
        if email_verification_code and request.session.get('email_verification_code') == email_verification_code:
            if photo:
                path = default_storage.save('photos/' + photo.name, ContentFile(photo.read()))
                photo_url = path
            else:
                photo_url = 'sample_images/basic_person.png'
            
            user = User.objects.create_user(
                username=email, 
                email=email, 
                password=password1,
                nickname=nickname,
                photo_url=photo_url,
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            user.set_password(password1)
            user.save()

            login(request, user)
            return redirect('user:select_artworks')
        else:
            return render(request, 'register.html', {'error': '유효하지 않은 인증 코드입니다.'})
    else:
        return render(request, 'register.html')

def register_seller(request):
    if request.method == 'POST':
        username = request.POST['email']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        nickname = request.POST['nickname']
        photo = request.FILES.get('photo')
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        bank = request.POST['bank']
        bank_user = request.POST['bank_user']
        account = request.POST['account']
        department_id = request.POST['department']
        department = Department.objects.get(id=department_id)
        
        if password1 != password2:
            return render(request, 'register_seller.html', {'error': 'Passwords do not match'})
        if Seller.objects.filter(email=email).exists():
            return render(request, 'register_seller.html', {'error': 'Email already taken'})
        
        if photo:
            path = default_storage.save('photos/' + photo.name, ContentFile(photo.read()))
            photo_url = path
        else:
            photo_url = 'photos/basic_person.png'
        
        password=make_password(password1)

        seller = Seller.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            nickname=nickname,
            photo_url=photo_url,
            phone_number=phone_number,
            password=password,
            bank=bank,
            bank_user=bank_user,
            account=account,
            department=department
        )
        login(request, seller)
        return redirect('user:select_artworks')
    
    departments = Department.objects.all()
    return render(request, 'register_seller.html', {'departments': departments})

def send_verification_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({'success': False, 'error': '이메일을 입력하세요.'})

        verification_code = generate_verification_code()
        request.session['email_verification_code'] = verification_code
        request.session['email'] = email
        send_verification_email(email, verification_code)
        
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': '유효하지 않은 요청입니다.'})

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.nickname = request.POST.get('nickname', user.nickname)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)

        photo = request.FILES.get('photo')
        
        if photo:
            # 새 파일 저장
            path = default_storage.save('photos/' + photo.name, ContentFile(photo.read()))
            user.photo_url = path
        # 'photo'가 없을 경우 기존 user.photo_url 값을 유지
        user.save()
        return redirect('user:update_profile')

    else:
        return render(request, 'update_profile.html')
    
@login_required
def update_seller_profile(request):
    user = request.user
    try:
        seller = Seller.objects.get(id=user.id)
    except Seller.DoesNotExist:
        return HttpResponse("Only sellers can update their information.")
    
    if request.method == 'POST':
        seller.nickname = request.POST.get('nickname', seller.nickname)
        seller.phone_number = request.POST.get('phone_number', seller.phone_number)
        seller.first_name = request.POST.get('first_name', seller.first_name)
        seller.last_name = request.POST.get('last_name', seller.last_name)
        seller.bank = request.POST.get('bank', seller.bank)
        seller.bank_user = request.POST.get('bank_user', seller.bank_user)
        seller.account = request.POST.get('account', seller.account)
        department_id = request.POST.get('department', seller.department.id)
        seller.department = Department.objects.get(id=department_id)

        photo = request.FILES.get('photo')
        
        if photo:
        # 새 파일 저장
            path = default_storage.save('photos/' + photo.name, ContentFile(photo.read()))
            seller.photo_url = path
        # 'photo'가 없을 경우 기존 seller.photo_url 값을 유지
        seller.save()
        return redirect('user:update_seller_profile')
    
    departments = Department.objects.all()
    return render(request, 'update_seller_profile.html', {'seller': seller, 'departments': departments})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def select_register(request):
    return render(request,'select_register.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if new password and confirm password match
        if new_password != confirm_password:
            return render(request, 'change_password.html', {'error': 'New password and confirm password do not match.'})
        
        # Check if current password matches
        user = request.user
        if not user.check_password(current_password):
            return render(request, 'change_password.html', {'error': 'Current password is incorrect.'})

        # Change password
        user.set_password(new_password)
        user.save()

        # Update session to reflect the password change
        login(request, user)

        return redirect('user:change_password')
    
    return render(request, 'change_password.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        agree = request.POST.get('agree')

        if password and agree:
            user = request.user

            # 비밀번호 검증
            if user.check_password(password):
                if agree == 'on':  # 동의 체크박스가 체크된 경우
                    user.delete()
                    logout(request)
                    return redirect('home')  # 탈퇴 후 리디렉션할 URL
                else:
                    return render(request, 'delete_account.html', {'error': 'You must agree to delete your account.'})
            else:
                return render(request, 'delete_account.html', {'error': 'Incorrect password.'})
        else:
            return render(request, 'delete_account.html', {'error': 'Please fill out all fields.'})

    return render(request, 'delete_account.html')

@login_required
def select_artworks(request):
    artworks = ArtWork.objects.all()  # 작품들을 가져옴

    if request.method == 'POST':
        selected_artworks = request.POST.getlist('artworks')  # 선택된 작품들의 ID 리스트를 가져옴
        user = request.user  # 현재 로그인한 사용자

        for artwork_id in selected_artworks:
            artwork = ArtWork.objects.get(id=artwork_id)
            UserPreferArt.objects.create(user=user, art_work=artwork)

        return redirect('home')  # 선택 완료 후 이동할 URL 설정
        
    return render(request, 'select_artworks.html', {'artworks': artworks})


def change_address(request):
    address_list = ShippingAddress.objects.filter(user_id=request.user.id, is_deleted=False)
    return render(request, 'change_address.html', {'address_list': address_list})

def create_address(request):
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
            else: detail_address =  request.POST.get('more_address')

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
            return redirect('user:change_address')
        else: 
            address_list = ShippingAddress.objects.filter(user_id=request.user.id, is_deleted=False)
            context = {
                'address_list': address_list,
                'error': '배송지 항목은 최대 5개까지 등록할 수 있습니다.'
            }
            return render(request, 'change_address.html', context)

def delete_address(request, pk):
    address = ShippingAddress.objects.get(pk=pk)
    address.is_deleted = True
    address.save()
    return redirect('user:change_address')

def update_address(request, pk):
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
        else: address.detail_address =  request.POST.get('more_address')

        is_default = request.POST.get('is_default')
        if is_default:
            ShippingAddress.objects.filter(user=request.user, is_default=True).update(is_default=False)
            address.is_default = True
        else:
            address.is_default = False

        address.save()
        return redirect('user:change_address')

def purchase_history(request):
    user = request.user
    order_complete_status = OrderStatus.objects.get(status='주문 완료')
    order_confirm_status = OrderStatus.objects.get(status='구매 확정')
    order_cancel_status = OrderStatus.objects.get(status='구매 취소')
    order_refund_status = OrderStatus.objects.get(status='환불 완료')

    orders = OrderItem.objects.filter(
        user=user,
        art_work__is_reservable=False,
        order_status__in=[order_complete_status, order_confirm_status, order_cancel_status, order_refund_status]
    ).order_by('-updated_at')

    paginator = Paginator(orders, 10)  # 페이지당 10개 항목
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'orders': page_obj,
    }
    return render(request, 'user/purchase_history.html', context)

def reservation_history(request):
    user = request.user
    order_complete_status = OrderStatus.objects.get(status='주문 완료')
    reserve_cancel_status = OrderStatus.objects.get(status='예약 취소')

    orders = OrderItem.objects.filter(
        user=user,
        art_work__is_reservable=True,
        order_status__in=[order_complete_status, reserve_cancel_status]
    ).order_by('-updated_at')

    paginator = Paginator(orders, 10)  # 페이지당 10개 항목
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'orders': page_obj,
    }
    return render(request, 'user/reservation_history.html', context)

@require_POST
def cancel_order(request, order_id):
    user = request.user
    order = get_object_or_404(OrderItem, id=order_id, user=user)
    order_cancel_status = OrderStatus.objects.get(status='구매 취소')
    order_complete_status = OrderStatus.objects.get(status='주문 완료')

    if order.order_status == order_complete_status:
        order.order_status = order_cancel_status
        order.save()
        order.art_work.is_sold = False
        order.art_work.save()
        messages.success(request, '주문이 성공적으로 취소되었습니다.')
    else:
        messages.error(request, '이 주문은 취소할 수 없습니다.')

    return redirect('user:purchase_history')

def cancel_reservation(request):
    if request.method == 'POST':
        order_item_ids = request.POST.getlist('order_items')
        order_cancel_status = OrderStatus.objects.get(status='예약 취소')

        for order_item_id in order_item_ids:
            order_item = get_object_or_404(OrderItem, id=order_item_id)
            order_item.order_status = order_cancel_status
            order_item.art_work.is_sold = False
            order_item.save()

        messages.success(request, '선택한 예약이 성공적으로 취소되었습니다.')
    
    return redirect('user:reservation_history')

# 구매 확정 이후 환불 (실제 정산은 아직 되기 전 일 수 있음)
@login_required
def request_refund(request, order_id):
    user = request.user
    order = get_object_or_404(OrderItem, id=order_id, user=user)
    payment_complete_status = PaymentStatus.objects.get(status='결제 완료')
    order_confirm_status = OrderStatus.objects.get(status='구매 확정')
    order_refund_status = OrderStatus.objects.get(status='환불 완료')

    if request.method == 'POST':
        # 결제가 완료되고, 구매 확정이 된 상품에 대해 환불 진행
        if order.payment.payment_status == payment_complete_status:
            if order.order_status == order_confirm_status:
                reason = request.POST.get('reason')
                # 입력 받은 정보로 환불서 작성
                refund_request = RefundRequest.objects.create(
                    reason = reason,
                    user = user,
                    order_item = order
                )
                # 환불서에 첨부된 사진 저장
                for file in request.FILES.getlist('refund_images'):
                    RefundImg.objects.create(
                        image_url=file,
                        refund_request=refund_request
                    )

                order.order_status = order_refund_status
                order.save()
                order.art_work.is_sold = False
                order.art_work.save()
                messages.success(request, '상품 환불이 정상적으로 완료되었습니다.')
            else:
                messages.error(request, '해당 상품은 이미 환불 되었거나, 환불할 수 없는 상태입니다. 문제가 반복되면 관리자에게 연락바랍니다.')
        
        return redirect('user:purchase_history')
    
    return render(request, 'user/refund_request.html', {'order': order})

def history_detail(request, order_id):
    order = get_object_or_404(OrderItem, id=order_id, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'user/history_detail.html', context)



