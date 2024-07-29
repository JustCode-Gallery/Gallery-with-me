from django.views.generic import ListView
from user.models import User 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from order.models import Cart

class HomeView(ListView):
    model = User
    template_name = 'home.html'
    context_object_name = 'objects'

# 현재 사용자의 장바구니에 담긴 아이템의 수
@login_required
def get_cart_count(request):
    cart_count = Cart.objects.filter(user=request.user).count()
    return JsonResponse({'cart_count': cart_count})