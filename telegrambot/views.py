from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from telegrambot.models import *
from telegrambot.serializers import TriggerSerializer
from django.contrib.auth.models import User
from telegrambot.serializers import *
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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BotList(APIView):
    """
    List all bots, or create a new snippet.
    """
    queryset = Telegrambot.objects.all()
    permission_classes = (OnlyOwner,)
    authentication_classes = (OAuth2Authentication, SocialAuthentication)

    def get(self, request, format=None):

        if self.request.user.username:
            serializer = TelegrambotSerializer(self.queryset.filter(user=self.request.user), many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, format=None):

        serializer = TelegrambotSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=self.request.user)
            except IntegrityError:
                return Response('Duplicated', status=status.HTTP_400_BAD_REQUEST)
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BotDetails(APIView):
    """
    Retrieve, update or delete a bot instance.
    """
    queryset = Telegrambot.objects.all()
    permission_classes = (OnlyOwner,)
    authentication_classes = (OAuth2Authentication, SocialAuthentication)
    
    def get_object(self, pk):
        try:
            obj = Telegrambot.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
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


class BehaviourList(APIView):
    queryset = Behaviour.objects.all()
    permission_classes = (OnlyOwner,)
    authentication_classes = (OAuth2Authentication, SocialAuthentication)

    def get(self, request, pk_bot, format=None):

        if self.request.user.username:
            try:
                bot = Telegrambot.objects.get(id=pk_bot, user=self.request.user)
            except Telegrambot.DoesNotExist:
                return Response('Bot does not exists', 404)

            serializer = BehaviourSerializer(self.queryset.filter(bot=bot), many=True)
            return Response(serializer.data)
        else:
            
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, pk_bot, format=None):
        
        serializer = BehaviourSerializer(data=request.data)
        try:
            bot = Telegrambot.objects.get(id=pk_bot, user=self.request.user)
        except Telegrambot.DoesNotExist:
            raise Http404

        if serializer.is_valid():
            try:
                serializer.save(bot=bot)
            except IntegrityError as e:
                print(e)
                return Response('Duplicated', status=status.HTTP_400_BAD_REQUEST)
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BehaviourDetail(APIView):
    queryset = Behaviour.objects.all()
    permission_classes = (OnlyOwner,)
    authentication_classes = (OAuth2Authentication, SocialAuthentication)
    
    def get_object(self, pk_bot, pk):
        try:
            try:
                bot = Telegrambot.objects.get(id=pk_bot)
            except Telegrambot.DoesNotExist:
                raise Http404
            self.check_object_permissions(self.request, bot)
            obj = Behaviour.objects.get(id=pk, bot=bot)

            return obj

        except Behaviour.DoesNotExist:
            raise Http404

    def get(self, request, pk_bot, pk, format=None):

        behaviour = self.get_object(pk_bot, pk)
        serializer = BehaviourSerializer(behaviour)
        return Response(serializer.data)


    def put(self, request, pk_bot, pk, format=None):

        behaviour = self.get_object(pk_bot, pk)
        serializer = BehaviourSerializer(behaviour, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk_bot, pk, format=None):

        behaviour = self.get_object(pk_bot, pk)
        behaviour.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TriggerList(APIView):
    queryset = Trigger.objects.all()
    permission_classes = (OnlyOwner,)
    authentication_classes = (OAuth2Authentication, SocialAuthentication)

    def get(self, request, pk_bot, pk_behaviour, format=None):

        if self.request.user.username:
            try:
                bot = Telegrambot.objects.get(id=pk_bot, user=self.request.user)
            except Telegrambot.DoesNotExist:
                return Response('Bot does not exists', 404)
            try:
                behaviour = Behaviour.objects.get(id=pk_behaviour)
            except Behaviour.DoesNotExist:
                return Response('Behaviour does not exists', 404)                

            serializer = TriggerSerializer(self.queryset.filter(behaviour=behaviour), many=True)
            return Response(serializer.data)
        else:
            
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, pk_bot, format=None):
        
        serializer = TriggerSerializer(data=request.data)
        try:
            bot = Telegrambot.objects.get(id=pk_bot, user=self.request.user)
        except Telegrambot.DoesNotExist:
            raise Http404

        if serializer.is_valid():
            try:
                serializer.save(bot=bot)
            except IntegrityError as e:
                print(e)
                return Response('Duplicated', status=status.HTTP_400_BAD_REQUEST)
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TriggerDetail(APIView):
    queryset = Trigger.objects.all()
    permission_classes = (OnlyOwner,)
    authentication_classes = (OAuth2Authentication, SocialAuthentication)
    
    def get_object(self, pk_bot, pk):
        try:
            try:
                bot = Telegrambot.objects.get(id=pk_bot)
            except Telegrambot.DoesNotExist:
                raise Http404
            self.check_object_permissions(self.request, bot)
            obj = Trigger.objects.get(id=pk, bot=bot)

            return obj

        except Trigger.DoesNotExist:
            raise Http404

    def get(self, request, pk_bot, pk, format=None):

        Trigger = self.get_object(pk_bot, pk)
        serializer = TriggerSerializer(Trigger)
        return Response(serializer.data)


    def put(self, request, pk_bot, pk, format=None):

        Trigger = self.get_object(pk_bot, pk)
        serializer = TriggerSerializer(Trigger, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk_bot, pk, format=None):

        Trigger = self.get_object(pk_bot, pk)
        Trigger.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

