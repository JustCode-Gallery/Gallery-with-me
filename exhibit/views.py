from django.shortcuts import render
import folium
from .models import ArtExhibit
from geopy.geocoders import Nominatim

def exhibit_list(request):
    exhibits = ArtExhibit.objects.all()
    context = {
        'exhibits': exhibits
    }
    return render(request, 'exhibit/exhibit_list.html', context)

def exhibit_map(request, exhibit_id):

    # ArtExhibit 객체 가져오기
    exhibit = ArtExhibit.objects.get(id=exhibit_id)
    
    # 주소를 위도와 경도로 변환
    geolocator = Nominatim(user_agent="art_exhibit_locator")
    location = geolocator.geocode(exhibit.address)
    lat = location.latitude
    lon = location.longitude

    # folium 객체 생성, Marker 추가
    figure = folium.Map(location=[lat, lon], zoom_start=17)
    folium.Marker(location=[lat, lon], popup=exhibit.title, icon=folium.Icon(color='blue', icon='info-sign')).add_to(figure)
    folium.CircleMarker(location=[lat, lon], radius=100, color='blue', fill_color='blue').add_to(figure)

    # folium 객체의 _repr_html() 메소드를 통해 html 출력할 수 있도록 객체화
    context = {
        'map': figure._repr_html_(),
        'title': exhibit.title,
        'description': exhibit.description,
        'start_date': exhibit.start_date,
        'end_date': exhibit.end_date,
        'address': exhibit.address,
    }

    return render(request, 'exhibit/exhibit_list.html', context)


map = folium.Map(location=[37, 127], zoom_start=10)