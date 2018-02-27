from django.conf.urls import url
from django.urls import path
from telegrambot import views

urlpatterns = [
    url(r'^triggers/$', views.TriggerList.as_view()),
    url(r'^triggers/(?P<pk>[0-9]+)/$', views.TriggerDetail.as_view()),
    url(r'^bots/$', views.BotList.as_view()),
    path('bots/<str:pk>/', views.BotDetails.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view())
]