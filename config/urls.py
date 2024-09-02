"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from config.views import HomeView, get_cart_count
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
      # 앱별 urls연결
    path('artwork/', include('artwork.urls')),
    path('board/', include('board.urls')),
    path('exhibit/', include('exhibit.urls')),
    path('order/', include('order.urls')),
    path('payment/', include('payment.urls')),
    path('user/', include('user.urls')),
    path('artist/', include('seller.urls')), # seller 앱에 artist_list_page 작성, url이 'seller/artist/' 부적절
    path('', HomeView.as_view(),name='home'), # 홈화면
    path('get-cart-count/', get_cart_count, name='get_cart_count'),
    path('accounts/', include('allauth.urls')), 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
