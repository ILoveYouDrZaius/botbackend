from rest_framework import serializers
from telegrambot.models import Trigger, Telegrambot, TRIGGERS_CHOICES
from django.contrib.auth.models import User


class TriggerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    behaviour = serializers.StringRelatedField(read_only=True)
    word_trigger = serializers.CharField(required=True, max_length=100)
    type_behaviour = serializers.ChoiceField(choices=TRIGGERS_CHOICES, required=False)

    def create(self, validated_data):
        """
        Create and return a new `Trigger` instance, given the validated data.
        """
        return Trigger.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Trigger` instance, given the validated data.
        """
        instance.behaviour = validated_data.get('behaviour', instance.behaviour)
        instance.word_trigger = validated_data.get('word_trigger', instance.word_trigger)
        instance.type_behaviour = validated_data.get('type_behaviour', instance.type_behaviour)
        instance.save()
        return instance

class TelegrambotSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    name = serializers.CharField(max_length=30)
    token = serializers.CharField(max_length=50)
    active = serializers.BooleanField()
    
    def create(self, validated_data):
        """
        Create and return a new `Telegrambot` instance, given the validated data.
        """
        return Telegrambot.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Telegrambot` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.token = validated_data.get('token', instance.token)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    # bots = serializers.PrimaryKeyRelatedField(many=True, queryset=Telegrambot.objects.all())
    bots = serializers.PrimaryKeyRelatedField(many=True, queryset=Telegrambot.objects.all())
    
    class Meta:
        model = User
        fields = ('id', 'username', 'bots')
        # fields = ('id', 'username')