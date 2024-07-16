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
            photo_url = 'sample_images/basic_person.png'
        
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









