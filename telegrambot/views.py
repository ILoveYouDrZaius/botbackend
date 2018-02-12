from django.shortcuts import render
from .models import Trigger
from rest_framework import serializers, viewsets

# Serializers define the API representation.
class TriggerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trigger
        fields = ('word_trigger','type_trigger')
        # fields = Trigger._meta.get_fields()

# ViewSets define the view behavior.
class TriggerViewSet(viewsets.ModelViewSet):
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer