from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from telegrambot.models import Trigger, Telegrambot
from telegrambot.serializers import TriggerSerializer
from django.contrib.auth.models import User
from telegrambot.serializers import UserSerializer, TelegrambotSerializer
from telegrambot.permissions import *
from telegram.error import InvalidToken

from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework_social_oauth2.authentication import SocialAuthentication

class UserList(APIView):
    """
    List or create a new user
    """
    queryset = User.objects.all()

    def get(self, request, format=None):
        serializer = UserSerializer(self.queryset)
        return Response(serializer.data)
    
    # @authentication_classes((OAuth2Authentication, SocialAuthentication))
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BotList(APIView):
    """
    List all bots, or create a new snippet.
    """
    queryset = Telegrambot.objects.all()
    permission_classes = (Deny,)
    authentication_classes = (OAuth2Authentication, SocialAuthentication)

    def get(self, request, format=None):
        if self.request.user.username:
            serializer = TelegrambotSerializer(self.queryset.filter(user=self.request.user), many=True)
            return Response(serializer.data)
        else:
            return Response('')

    def post(self, request, format=None):

        serializer = TelegrambotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BotDetails(APIView):
    """
    Retrieve, update or delete a bot instance.
    """
    queryset = Telegrambot.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, OnlyOwner)

    def get_object(self, pk):
        try:
            return Telegrambot.objects.get(pk=pk)
        except Telegrambot.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):

        bot = self.get_object(pk)
        serializer = TelegrambotSerializer(bot)
        return Response(serializer.data)


    def put(self, request, pk, format=None):

        bot = self.get_object(pk)
        serializer = TelegrambotSerializer(bot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):

        bot = self.get_object(pk)
        bot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TriggerList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, OnlyOwner)
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer


class TriggerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, OnlyOwner)
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer