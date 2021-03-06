"""botbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from telegrambot import views
# from telegrambot.views import TriggerViewSet

# router = routers.DefaultRouter()
# router.register(r'triggers', TriggerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('telegrambot.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    # url(r'^admin/', include(admin.site.urls)),
]
