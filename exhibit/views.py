from django.shortcuts import render, redirect
import folium
from .models import ArtExhibit, ExhibitBookmark, ArtExhibitPoster
from .forms import ArtExhibitForm, ArtExhibitPosterForm
from django.core.paginator import Paginator
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ArtExhibitSerializer
from django.db.models import Q

def exhibit_list(request):
    query = request.GET.get('query', '')
    user = request.user if request.user.is_authenticated else None

    # 검색을 한 경우 관련 결과 출력
    if query:
        # 전시제목, 학교, 학과 등으로 검색 가능
        exhibits = ArtExhibit.objects.filter(
        Q(title__icontains=query) |
        Q(university_department__university__name__icontains=query) |
        Q(university_department__department__name__icontains=query)
        )
    else:
        exhibits = ArtExhibit.objects.all()

    # 페이지네이션 설정
    paginator = Paginator(exhibits, 5)  # 한 페이지에 10개씩 보이도록 설정
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

    poster = ArtExhibitPoster.objects.filter(exhibit_id=exhibit.id)    

    context = {
        'id': exhibit.id,
        'title': exhibit.title,
        'description': exhibit.description,
        'start_date': exhibit.start_date,
        'end_date': exhibit.end_date,
        'address': exhibit.address,
        'university_department': exhibit.university_department,
        'is_bookmarked': is_bookmarked,
        'map': figure._repr_html_(), # folium 객체의 _repr_html() 메소드를 통해 html 출력할 수 있도록 객체화
        'poster': poster,
    }

    return render(request, 'exhibit/exhibit_detail.html', context)

def create_exhibit(request):
    if request.method == 'POST':
            form = ArtExhibitForm(request.POST)
            formset = ArtExhibitPosterForm(request.POST, request.FILES) # 포스터 추가
            if form.is_valid():
                exhibit = form.save()

                images = request.FILES.getlist('image',None)

                for image in images:
                    ArtExhibitPoster.objects.create(exhibit=exhibit, poster_url=image)

                return redirect('exhibit:exhibit_list')
            else:
                # 폼이 유효하지 않은 경우 에러 메시지 출력
                print(form.errors)
                print(formset.errors)
    else:
        form = ArtExhibitForm()
        formset = ArtExhibitPosterForm() # 포스터 추가

    return render(request, 'exhibit/form.html', {'form': form, 'formset': formset})

@api_view(['POST'])
def create_exhibit_api(request):
    serializer = ArtExhibitSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def exhibit_like_list(request):
    like_list = ExhibitBookmark.objects.filter(user=request.user)
    context = {
        'like_list': like_list,
    }
    return render(request, 'exhibit/exhibit_like_list.html', context)

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

    print("This was not a ajax function")
    return JsonResponse({'is_bookmarked': is_bookmarked})
