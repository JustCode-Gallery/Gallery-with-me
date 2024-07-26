from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Cart
# Create your views here.

@login_required
def cart_list(request):
    user = request.user
    carts = Cart.objects.filter(user=user).select_related('art_work').prefetch_related('art_work__artimage_set')

    content = {
        'carts' : carts
    }
    return render(request, 'order/cart.html', content)

@login_required
def delete_cart_item(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    # 카트 뱃지 비동기 업데이트를 위해 아이템 수 가져옴
    cart_count = Cart.objects.filter(user=request.user).count()
    return JsonResponse({'success': True, 'cart_count': cart_count})