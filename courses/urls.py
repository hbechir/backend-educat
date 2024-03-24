from django.urls import path
from . import views

urlpatterns = [
    path('', views.getCoursesByFilters),
    path('add/', views.addCourse),
]
