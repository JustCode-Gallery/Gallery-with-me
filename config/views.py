from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from user.models import User, UserPreferArt
from artwork.models import ArtWork, ArtTag
from order.models import Cart
from django.db.models import Count, Q
from django.shortcuts import render
from django.urls import reverse
import json

class HomeView(ListView):
    model = User
    template_name = 'home.html'
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            user = self.request.user

            # 유저의 선호 작품들을 가져오기
            preferred_artworks = UserPreferArt.objects.filter(user=user).values_list('art_work', flat=True)

            # 선호 작품들의 태그들을 가져오기
            preferred_tags = ArtTag.objects.filter(art_work__in=preferred_artworks).values_list('tag', flat=True)

            # 유사한 작품들을 검색 (선호 작품들은 제외)
            recommended_artworks = ArtWork.objects.filter(
                arttag__tag__in=preferred_tags
            ).exclude(
                id__in=preferred_artworks
            ).annotate(
                matching_tags_count=Count('arttag__tag', filter=Q(arttag__tag__in=preferred_tags))
            ).order_by('-matching_tags_count')[:10]

            # 디버그: 각 작품의 ID를 출력
            for artwork in recommended_artworks:
                print(f"ArtWork ID: {artwork.id}, Title: {artwork.title}")

            # JSON으로 변환하여 전달
            context['recommended_artworks_json'] = json.dumps([
                {
                    'imageUrl': artwork.artimage_set.first().image_url.url if artwork.artimage_set.exists() else '',
                    'title': artwork.title,
                    'price': str(artwork.price),
                    'description': artwork.description,
                    'detailLink': reverse('artwork:artwork_detail', args=[artwork.id])
                } for artwork in recommended_artworks
            ])

            print('recommended list : ',context)

        return context
# 현재 사용자의 장바구니에 담긴 아이템의 수
@login_required
def get_cart_count(request):
    cart_count = Cart.objects.filter(user=request.user).count()
    return JsonResponse({'cart_count': cart_count})