from .models import Cart

# 컨텍스트 프로세서 : request 객체를 인자로 받아 딕셔너리를 반환하는 함수
def cart_count(request):
    if request.user.is_authenticated:
        return {'cart_count': Cart.objects.filter(user=request.user).count()}
    return {'cart_count': 0}