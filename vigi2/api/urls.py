from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # Route for API overview
    path('', views.getRoutes),

    # Route for listing and creating series
    path('series/', views.series_list),

    # Route for retrieving, updating, and deleting a specific series by its primary key
    path('series/<int:pk>/', views.series_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
