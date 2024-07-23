from django.shortcuts import render, redirect
import folium
from .models import ArtExhibit, ExhibitBookmark
from .forms import ArtExhibitForm
from django.core.paginator import Paginator
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def exhibit_list(request):
    query = request.GET.get('query', '')
    user = request.user if request.user.is_authenticated else None

    # 검색을 한 경우 관련 결과 출력
    if query:
            exhibits = ArtExhibit.objects.filter(title__icontains=query)
    else:
        exhibits = ArtExhibit.objects.all()

    # 페이지네이션 설정
    paginator = Paginator(exhibits, 10)  # 한 페이지에 10개씩 보이도록 설정
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 모든 전시의 위치정보를 리스트에 저장
    locations = []
    for exhibit in page_obj:
        locations.append({
            'id': exhibit.id,
            'title': exhibit.title,
            'latitude': float(exhibit.latitude),  # Decimal을 float로 변환
            'longitude': float(exhibit.longitude),
            'is_bookmarked': ExhibitBookmark.objects.filter(user=user, exhibit=exhibit).exists() if user else False  # 북마크 상태 추가
        })

    # # 각 전시에 북마크 상태 추가
    # for exhibit in page_obj:
    #     exhibit.is_bookmarked = ExhibitBookmark.objects.filter(user=user, exhibit=exhibit).exists()

    context = {
        'exhibits': page_obj,
        'locations': json.dumps(locations, cls=DjangoJSONEncoder) # json으로 명시적으로 변환해서 보내야 오류 없음
    }
    return render(request, 'exhibit/exhibit_list.html', context)

def exhibit_detail(request, exhibit_id):
    # ArtExhibit 객체 가져오기
    exhibit = ArtExhibit.objects.get(id=exhibit_id)
    user = request.user if request.user.is_authenticated else None

    # 해당 전시의 북마크 여부 가져오기
    is_bookmarked = ExhibitBookmark.objects.filter(user=user, exhibit=exhibit).exists() if user else False 

    # folium 객체 생성, Marker 추가
    figure = folium.Map(location=[exhibit.latitude, exhibit.longitude], zoom_start=17)
    folium.Marker(location=[exhibit.latitude, exhibit.longitude], popup=exhibit.title, icon=folium.Icon(color='blue', icon='info-sign')).add_to(figure)
    folium.CircleMarker(location=[exhibit.latitude, exhibit.longitude], radius=100, color='blue', fill_color='blue').add_to(figure)

    context = {
        'id': exhibit.id,
        'title': exhibit.title,
        'description': exhibit.description,
        'start_date': exhibit.start_date,
        'end_date': exhibit.end_date,
        'address': exhibit.address,
        'is_bookmarked': is_bookmarked,
        'map': figure._repr_html_(), # folium 객체의 _repr_html() 메소드를 통해 html 출력할 수 있도록 객체화
    }

    return render(request, 'exhibit/exhibit_detail.html', context)

def create_exhibit(request):
    if request.method == 'POST':
        form = ArtExhibitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exhibit:exhibit_list')
        else:
            # 폼이 유효하지 않은 경우 에러 메시지 출력
            print(form.errors)
    else:
        form = ArtExhibitForm()
    return render(request, 'exhibit/form.html', {'form': form})

# 사용자가 해당 전시를 북마크할 수 있음
@login_required
def exhibit_bookmark(request, exhibit_id):
    user = request.user
    exhibit = ArtExhibit.objects.get(id=exhibit_id)
    
    exhibit_bookmark, created = ExhibitBookmark.objects.get_or_create(user=user, exhibit=exhibit)
    if created: # 북마크되지 않았던 전시라면 북마크함(레코드 생성)
        is_bookmarked = True
    else: # 북마크 되어있던 전시라면 북마크 취소함(레코드 삭제)
        exhibit_bookmark.delete()
        is_bookmarked = False

    # # AJAX 요청 처리
    # if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #     print("this is ajax")
    #     return JsonResponse({'is_bookmarked': is_bookmarked})

    print("This was not a ajax function")
    #return redirect('exhibit:exhibit_detail', exhibit_id=exhibit_id)
    return JsonResponse({'is_bookmarked': is_bookmarked})