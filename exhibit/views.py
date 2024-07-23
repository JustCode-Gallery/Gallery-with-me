from django.shortcuts import render, redirect
import folium
from .models import ArtExhibit, ExhibitBookmark
from .forms import ArtExhibitForm
from django.core.paginator import Paginator
import json
from django.core.serializers.json import DjangoJSONEncoder

def exhibit_list(request):
    exhibits = ArtExhibit.objects.all()

    # 페이지네이션 설정
    paginator = Paginator(exhibits, 10)  # 한 페이지에 10개씩 보이도록 설정
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    locations = []
    for exhibit in page_obj:
            locations.append({
                'id' : exhibit.id,
                'title': exhibit.title,
                'latitude': float(exhibit.latitude),  # Decimal을 float로 변환
                'longitude': float(exhibit.longitude)  
            })
    
    context = {
        'exhibits': page_obj,
        'locations': json.dumps(locations, cls=DjangoJSONEncoder)
    }
    return render(request, 'exhibit/exhibit_list.html', context)

def exhibit_detail(request, exhibit_id):
    # ArtExhibit 객체 가져오기
    exhibit = ArtExhibit.objects.get(id=exhibit_id)

    # folium 객체 생성, Marker 추가
    figure = folium.Map(location=[exhibit.latitude, exhibit.longitude], zoom_start=17)
    folium.Marker(location=[exhibit.latitude, exhibit.longitude], popup=exhibit.title, icon=folium.Icon(color='blue', icon='info-sign')).add_to(figure)
    folium.CircleMarker(location=[exhibit.latitude, exhibit.longitude], radius=100, color='blue', fill_color='blue').add_to(figure)

    # folium 객체의 _repr_html() 메소드를 통해 html 출력할 수 있도록 객체화
    context = {
        'map': figure._repr_html_(),
        'title': exhibit.title,
        'description': exhibit.description,
        'start_date': exhibit.start_date,
        'end_date': exhibit.end_date,
        'address': exhibit.address,
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

def exhibit_like_list(request):
    like_list = ExhibitBookmark.objects.filter(user=request.user)
    context = {
        'like_list': like_list,
    }
    return render(request, 'exhibit/exhibit_like_list.html', context)