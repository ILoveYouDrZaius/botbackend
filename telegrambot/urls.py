from django.conf.urls import url
from django.urls import path
from telegrambot import views

urlpatterns = [
    path('bots/', views.BotList.as_view()),
    path('bot/<str:pk>/', views.BotDetails.as_view()),

    path('bot/<str:pk_bot>/behaviours/', views.BehaviourList.as_view()),
    path('bot/<str:pk_bot>/behaviour/<str:pk>/', views.BehaviourDetail.as_view()),

    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]