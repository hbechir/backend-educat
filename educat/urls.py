"""
URL configuration for educat project.

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
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('dj-rest-auth/password/reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('questions/', include('questions.urls')),
    path('user/', include('user.urls')),
    path('base/', include('BASE.urls')),
    path('courses/', include('courses.urls')),
    path('gifts/', include('gifts.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
