from django.urls import path
from . import views

urlpatterns = [
    path('get-all-regions/', views.getAllRegions),
    path('get-all-school-types/', views.getAllSchoolTypes),
    path('get-schools-by-region-and-type/', views.getSchoolsByRegionAndType),
    path('get-grade-subjects/', views.getGradeSubjects),
    path('get-grades-by-school-type/', views.getGradesBySchoolType),
]
