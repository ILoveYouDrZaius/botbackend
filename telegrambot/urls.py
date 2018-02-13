from django.conf.urls import url
from telegrambot import views

urlpatterns = [
    url(r'^triggers/$', views.trigger_list),
    url(r'^triggers/(?P<pk>[0-9]+)/$', views.trigger_detail),
    url(r'^bots/$', views.BotList.as_view()),
    url(r'^bots/(?P<pk>[0-9]+)/$', views.BotDetails.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view())
]