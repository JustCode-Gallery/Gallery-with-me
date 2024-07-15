from django.shortcuts import render, redirect
import folium
from .models import ArtExhibit
from .forms import ArtExhibitForm
from geopy.geocoders import Nominatim
import json
from django.core.serializers.json import DjangoJSONEncoder

def exhibit_list(request):
    exhibits = ArtExhibit.objects.all()

    locations = []
    for exhibit in exhibits:
            locations.append({
                'title': exhibit.title,
                'latitude': float(exhibit.latitude),  # Decimal을 float로 변환
                'longitude': float(exhibit.longitude)  
            })
    
    context = {
        'exhibits': exhibits,
        'locations': json.dumps(locations, cls=DjangoJSONEncoder)
    }
    return render(request, 'exhibit/exhibit_list.html', context)

def exhibit_map(request, exhibit_id):
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