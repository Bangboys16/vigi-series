# vigiseries/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.series_list, name='series_list'),
    path('series/<slug:slug>/', views.series_detail, name='series_detail'),
    path('series/<slug:series_slug>/episode/<slug:episode_slug>/', views.episode_detail, name='episode_detail'),
    path('category/<str:category>/', views.category_list, name='category_list'),
]
