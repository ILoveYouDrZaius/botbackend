from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from telegrambot.models import Trigger, Telegrambot
from telegrambot.serializers import TriggerSerializer
from django.contrib.auth.models import User
from telegrambot.serializers import UserSerializer, TelegrambotSerializer
from telegrambot.permissions import IsOwnerOrReadOnly
from telegram.error import InvalidToken

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class BotList(generics.ListCreateAPIView):
#     queryset = Telegrambot.objects.all()
#     serializer_class = TelegrambotSerializer
#     # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

#     def perform_create(self, serializer):
        
#         if Telegrambot.test_token(serializer.validated_data.get('token')):
#             serializer.save(user=self.request.user)
#         else:
#             print('OK')
#             return HttpResponse('Mal', status=400)

# @api_view(['GET', 'POST'])
# def BotList(request):
#     if request.method == 'GET':
#         queryset = User.objects.all()
#         bots = Telegrambot.objects.filter(request.user)
#         serializer = TelegrambotSerializer(bots)

#         return Response(serializer.data)

class BotList(APIView):
    """
    List all bots, or create a new snippet.
    """
    queryset = Telegrambot.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):

        serializer = TelegrambotSerializer(self.queryset.all(), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TelegrambotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class BotDetails(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Telegrambot.objects.all()
#     serializer_class = TelegrambotSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

@csrf_exempt
def trigger_list(request):
    """
    List all triggers, or create a new trigger.
    """
    if request.method == 'GET':
        triggers = Trigger.objects.all()
        serializer = TriggerSerializer(triggers, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TriggerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def trigger_detail(request, pk):
    """
    Retrieve, update or delete a trigger.
    """
    try:
        trigger = Trigger.objects.get(pk=pk)
    except Trigger.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TriggerSerializer(trigger)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TriggerSerializer(trigger, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        trigger.delete()
        return HttpResponse(status=204)