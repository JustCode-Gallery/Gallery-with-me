from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import ArtWork, WorkLike, ArtistInquiry, TagCategory, Material, ArtImage
from order.models import Cart, Reservation
from user.models import User,Seller
from exhibit.models import ArtExhibit
from .forms import ArtWorkFilterForm, ArtistInquiryForm, ArtWorkSearchForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import requests

PAGINATE_BY = 10

class ArtWorkListView(ListView):
    model = ArtWork
    template_name = 'artwork/artwork_list.html'
    context_object_name = 'artwork_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort_by', 'recent')
        query = self.request.GET.get('query', '')

        if sort_by == 'high_price':  # 가격 높은순
            queryset = queryset.order_by('-price')
        elif sort_by == 'low_price':  # 가격 낮은순
            queryset = queryset.order_by('price')
        elif sort_by == 'recent':  # 최근 등록순
            queryset = queryset.order_by('-created_at')

        # URL 쿼리스트링을 통한 태그 필터링
        tag_param = self.request.GET.get('tags')
        if tag_param:
            tag_names = tag_param.split(',')
            queryset = queryset.filter(arttag__tag__name__in=tag_names).distinct()

        # URL 쿼리스트링을 통한 재료 필터링
        material_param = self.request.GET.get('materials')
        if material_param:
            material_names = material_param.split(',')
            queryset = queryset.filter(artworkmaterial__material__name__in=material_names).distinct()

        # URL 쿼리스트링을 통한 가격 필터링 (만원 단위를 원 단위로 변환)
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        if price_min is not None and price_max is not None:
            price_min = float(price_min) * 10000
            price_max = float(price_max) * 10000
            queryset = queryset.filter(price__gte=price_min, price__lte=price_max)

        # URL 쿼리스트링을 통한 너비 필터링
        width_min = self.request.GET.get('width_min')
        width_max = self.request.GET.get('width_max')
        if width_min is not None and width_max is not None:
            queryset = queryset.filter(width__gte=width_min, width__lte=width_max)

        # URL 쿼리스트링을 통한 높이 필터링
        height_min = self.request.GET.get('height_min')
        height_max = self.request.GET.get('height_max')
        if height_min is not None and height_max is not None:
            queryset = queryset.filter(height__gte=height_min, height__lte=height_max)

        # 검색 결과와 결합
        if query:
            response = requests.post(
                'http://127.0.0.1:8001/search/',
                json={'query': query}
            )
            if response.status_code == 200:
                search_results = response.json().get('results', [])
                if search_results:
                    search_titles = [result['title'] for result in search_results]
                    queryset = queryset.filter(title__in=search_titles)

        return queryset.filter(is_sold=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ArtWorkFilterForm()
        context['search_form'] = ArtWorkSearchForm()
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
            'image_url': artwork.artimage_set.first().image_url.url if artwork.artimage_set.first() else ''
        }
        for artwork in page_obj
    ]
    
    return JsonResponse({
        'artworks': artworks_data,
        'has_next': page_obj.has_next()  # 다음 페이지가 있는지 여부를 반환
    })
    
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

    # AJAX 요청인지 확인
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'count': artwork.worklike_set.count()})

    return redirect('artwork_detail', pk=pk)

@login_required
def add_to_cart(request, pk): # 장바구니에 담기 기능
    artwork = get_object_or_404(ArtWork, pk=pk)
    user = request.user

    # 기존에 담겨있는 항목인지 확인
    if Cart.objects.filter(user=user, art_work=artwork).exists():
        request.session['cart_message'] = '이미 장바구니에 있는 아이템입니다.'
        request.session['cart_message_type'] = 'info'
    else:
        # 장바구니에 추가
        Cart.objects.create(user=user, art_work=artwork)
        request.session['cart_message'] = '장바구니에 추가되었습니다.'
        request.session['cart_message_type'] = 'success'
        
    return redirect('artwork:artwork_detail', pk=pk)

@login_required
def buy_now(request, pk): # 바로 구매 기능
    # 추후 결제 페이지로 리다이렉트할 예정, 현재는 임시로 상세 페이지로 리다이렉트
    return redirect('artwork:artwork_detail', pk=pk)

@login_required
def add_inquiry(request, pk):  # 작가 문의하기 기능
    artwork = get_object_or_404(ArtWork, pk=pk)
    user = request.user

    if request.method == 'POST':
        form = ArtistInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.user = user
            inquiry.seller = artwork.seller
            inquiry.save()
            return redirect('artwork:artwork_detail', pk=pk)
        else: 
            messages.error(request, '문의 내용을 입력해주세요.')
    else:
        form = ArtistInquiryForm()

    return render(request, 'artwork/artwork_detail_add_inquiry.html', {'form': form, 'artwork': artwork})

@login_required
def reserve_artwork(request, pk): # 예약하기 기능
    artwork = get_object_or_404(ArtWork, pk=pk)
    user = request.user

    if artwork.is_reservable:
        # 구매 예약 생성
        Reservation.objects.create(user=user, art_work=artwork)
        return redirect('artwork:artwork_detail', pk=pk)
    else:
        # 예약이 불가능한 경우 처리(추가해야함)
        return redirect('artwork:artwork_detail', pk=pk)

def tag_material_categories_api(request):
    tag_categories = TagCategory.objects.all()
    material_categories = Material.objects.all()
    
    data = {
        'tag_categories': [
            {
                'name': category.name,
                'tags': [{'name': tag.name} for tag in category.tag_set.all()]
            }
            for category in tag_categories
        ],
        'materials': [{'name': material.name} for material in material_categories]
    }
    
    return JsonResponse(data, safe=False)


#작품 생성하기
@login_required
def create_artwork(request):
    if request.method == 'POST':
        #판매자가 입력한 값들 받아오기
        title = request.POST.get('title')
        description = request.POST.get('description')
        width = request.POST.get('width')
        height = request.POST.get('height')
        depth = request.POST.get('depth')
        year = request.POST.get('year')
        price = request.POST.get('price')
        exhibit_id = request.POST.get('exhibit')
        is_sold = request.POST.get('is_sold') == 'on'
        is_reservable = request.POST.get('is_reservable') == 'on'
        images = request.FILES.getlist('images')

        user = request.user

        #등록된 판매자인지 판단하기
        try:
            seller = Seller.objects.get(id=user.id)
        except Seller.DoesNotExist:
            return render(request, 'artwork/create_artwork.html', {
                'error_message': '등록된 판매자를 찾을 수 없습니다'
            })

        #등록된 전시회인지 판단하기
        exhibit = ArtExhibit.objects.get(id=exhibit_id) if exhibit_id else None

        #artwork생성
        try:
            artwork = ArtWork(
                title=title,
                description=description,
                width=int(width),
                height=int(height),
                depth=int(depth),
                year=int(year),
                price=price,
                seller=seller,
                exhibit=exhibit,
                is_sold=is_sold,
                is_reservable=is_reservable,
            )
            artwork.save()
            
            #artimage생성
            for image in images:
                ArtImage.objects.create(artwork=artwork, image_url=image)

            #성공시 리디헥션
            return redirect('artwork:seller_artwork_list')
        except ValueError:
            return render(request, 'artwork/create_artwork.html', {
                'error_message': '잘못된 정보가 들어가 있습니다. 다시 시도해주세요.'
            })

    seller = Seller.objects.filter(id=request.user.id)
    exhibits = ArtExhibit.objects.all()
    return render(request, 'artwork/create_artwork.html', {'seller': seller, 'exhibits': exhibits})


@login_required
def update_artwork(request, artwork_id):
    artwork = get_object_or_404(ArtWork, id=artwork_id)
    images = ArtImage.objects.filter(artwork=artwork)
    exhibits = ArtExhibit.objects.all()

    if request.method == 'POST':
        # 판매자가 입력한 값들 받아오기
        artwork.title = request.POST.get('title')
        artwork.description = request.POST.get('description')
        artwork.width = request.POST.get('width')
        artwork.height = request.POST.get('height')
        artwork.depth = request.POST.get('depth')
        artwork.year = request.POST.get('year')
        artwork.price = request.POST.get('price')
        artwork.exhibit_id = request.POST.get('exhibit')
        artwork.is_sold = request.POST.get('is_sold') == 'on'
        artwork.is_reservable = request.POST.get('is_reservable') == 'on'
        artwork.save()

        # 삭제할 이미지 처리
        deleted_images = request.POST.get('deleted_images')
        if deleted_images:
            image_ids_list = [img_id for img_id in deleted_images.split(',') if img_id]
            ArtImage.objects.filter(id__in=image_ids_list).delete()

        # 새로운 ArtImage 생성
        for file in request.FILES.getlist('images'):
            ArtImage.objects.create(artwork=artwork, image_url=file)

        return redirect('artwork:seller_artwork_list')

    context = {
        'artwork': artwork,
        'images': images,
        'exhibits': exhibits,
    }
    return render(request, 'artwork/update_artwork.html', context)

@login_required
def seller_artwork_list(request):
    seller = get_object_or_404(Seller, id=request.user.id)
    artworks= ArtWork.objects.filter(seller=seller)
    return render(request,  'artwork/seller_artwork_list.html', {'artworks':artworks,'seller':seller})

@login_required
def delete_artwork(request, artwork_id):
    seller = get_object_or_404(Seller, id=request.user.id)
    artwork = ArtWork.objects.filter(id=artwork_id,seller=seller)
    artwork.delete()
    return redirect('artwork:seller_artwork_list')

