from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from telegrambot.models import Trigger, Telegrambot
from telegrambot.serializers import TriggerSerializer
from django.contrib.auth.models import User
from telegrambot.serializers import UserSerializer, TelegrambotSerializer
from telegrambot.permissions import IsOwnerOrReadOnly

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BotList(generics.ListCreateAPIView):
    queryset = Telegrambot.objects.all()
    serializer_class = TelegrambotSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BotDetails(generics.RetrieveAPIView):
    queryset = Telegrambot.objects.all()
    serializer_class = TelegrambotSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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