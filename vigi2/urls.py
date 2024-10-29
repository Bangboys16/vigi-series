# vigiseries/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.series_list, name='series_list'),
    path('series/<int:pk>/', views.series_detail, name='series_detail'),
    path('series/<int:series_pk>/episode/<int:episode_pk>/', views.episode_detail, name='episode_detail'),
    path('category/<str:category>/', views.category_list, name='category_list'),
]
