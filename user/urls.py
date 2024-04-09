from django.urls import path
from . import views

urlpatterns = [
    path('finish-profile/', views.FinishProfile, name='finish-profile'),
    path('check-profile/', views.checkProfile, name='check-profile'),
    path('register/', views.register, name='register'),
    path('verify/', views.verify, name='verify'),
    path('send-code/', views.send_code, name='send_code'),

]
