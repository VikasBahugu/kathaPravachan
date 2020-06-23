from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('singlepost', views.singlepost, name='singlepost'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('videoblog', views.videoblog, name='videoblog'),
]
