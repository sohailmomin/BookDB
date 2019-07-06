from django.contrib import admin
from django.urls import path, include,re_path
from django.views.generic.base import TemplateView
from django.contrib.flatpages import views as flat_views

urlpatterns = [
    
    path('admin/', admin.site.urls),
     
    path('users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('',include('main.urls')),
    re_path(r'^about/$', flat_views.flatpage, {'url': '/about/'}, name='about'),

]