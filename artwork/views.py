from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import ArtWork, WorkLike, ArtistInquiry
from order.models import Cart, Reservation
from .forms import ArtWorkFilterForm, ArtistInquiryForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

PAGINATE_BY = 10

class ArtWorkListView(ListView):
    model = ArtWork
    template_name = 'artwork_list.html'
    context_object_name = 'artwork_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort_by', 'recent')
        
        if sort_by == 'high_price': # 가격 높은순
            queryset = queryset.order_by('-price')
        elif sort_by == 'low_price': # 가격 낮은순
            queryset = queryset.order_by('price')
        elif sort_by == 'recent': # 최근 등록순
            queryset = queryset.order_by('-created_at')
        
        # 검색 폼 데이터 처리
        form = ArtWorkFilterForm(self.request.GET)
        if form.is_valid():
            for field_name, field_value in form.cleaned_data.items():
                if field_value:
                    queryset = queryset.filter(**{field_name: field_value})

        return queryset.filter(is_sold = False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ArtWorkFilterForm()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context['artwork_list'] = self.get_queryset()
        return context
    
def load_more_artworks(request):
    page = request.GET.get('page', 1)
    artworks = ArtWork.objects.filter(is_sold=False)
    paginator = Paginator(artworks, 10)  # 페이지당 10개 항목
    page_obj = paginator.get_page(page)
    
    artworks_data = [
        {
            'id': artwork.id,
            'title': artwork.title,
            'price': artwork.price,
            'image_url': artwork.artimage_set.first().image.url if artwork.artimage_set.first() else ''
        }
        for artwork in page_obj
    ]
    
    return JsonResponse({'artworks': artworks_data})
    
class ArtWorkDetailView(DetailView):
    model = ArtWork
    template_name = 'artwork/artwork_detail.html'
    context_object_name = 'artwork'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artwork = self.get_object()
        user = self.request.user
        if user.is_authenticated:
            try:
                context['liked'] = artwork.worklike_set.filter(user=user).exists()
            except Exception as e:
                context['liked'] = False
                context['error'] = str(e)
        else:
            context['liked'] = False
        return context


@login_required
def toggle_work_like(request, pk): # 좋아요 기능
    artwork = get_object_or_404(ArtWork, pk=pk)
    user = request.user

    if WorkLike.objects.filter(user=user, art_work=artwork).exists():
        WorkLike.objects.filter(user=user, art_work=artwork).delete()
        liked = False
    else:
        WorkLike.objects.create(user=user, art_work=artwork)
        liked = True

    if request.is_ajax(): # AJAX로 좋아요 하기
        return JsonResponse({'liked': liked, 'count': artwork.worklike_set.count()})

    return redirect('artwork_detail', pk=pk)

@login_required
def add_to_cart(request, pk): # 장바구니에 담기 기능
    artwork = get_object_or_404(ArtWork, pk=pk)
    user = request.user

    # 장바구니에 추가
    Cart.objects.create(user=user, art_work=artwork)
    return redirect('artwork_detail', pk=pk)

@login_required
def buy_now(request, pk): # 바로 구매 기능
    # 추후 결제 페이지로 리다이렉트할 예정, 현재는 임시로 상세 페이지로 리다이렉트
    return redirect('artwork_detail', pk=pk)

@login_required
def add_inquiry(request, pk): # 작가 문의하기 기능
    artwork = get_object_or_404(ArtWork, pk=pk)
    user = request.user

    if request.method == 'POST':
        form = ArtistInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.user = user
            inquiry.seller = artwork.seller
            inquiry.save()
            return redirect('artwork_detail', pk=pk)
        else: messages.error(request, '문의 내용을 입력해주세요.')
    else:
        form = ArtistInquiryForm()

    return render(request, 'artwork_detail_add_inquiry.html', {'form': form, 'artwork': artwork})

@login_required
def reserve_artwork(request, pk): # 예약하기 기능
    artwork = get_object_or_404(ArtWork, pk=pk)
    user = request.user

    if artwork.is_reservable:
        # 구매 예약 생성
        Reservation.objects.create(user=user, art_work=artwork)
        return redirect('artwork_detail', pk=pk)
    else:
        # 예약이 불가능한 경우 처리(추가해야함)
        return redirect('artwork_detail', pk=pk)