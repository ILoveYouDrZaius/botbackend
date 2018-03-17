from rest_framework import serializers, permissions
from rest_framework.exceptions import ValidationError
from telegrambot.models import *
from django.contrib.auth.models import User


class TelegrambotSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    name = serializers.CharField(max_length=30, required=False)
    token = serializers.CharField(max_length=50, required=False)
    active = serializers.BooleanField(required=False)
    
    def create(self, validated_data):
        """
        Create and return a new `Telegrambot` instance, given the validated data.
        """
        if validated_data.get('token'):

            return Telegrambot.objects.create(**validated_data)
        else:
            error_dict = dict()
            error_dict['token'] = list()
            error_dict['token'].append('This field is required.')
            raise ValidationError(error_dict)
        # return Telegrambot.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Telegrambot` instance, given the validated data.
        """
        # instance.name = validated_data.get('name', instance.name)
        # instance.token = validated_data.get('token', instance.token)
        if validated_data.get('active'):
            instance.active = validated_data.get('active')
            instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    # bots = serializers.PrimaryKeyRelatedField(many=True, queryset=Telegrambot.objects.all())
    bots = serializers.PrimaryKeyRelatedField(many=True, queryset=Telegrambot.objects.all())
    
    class Meta:
        model = User
        fields = ('id', 'username', 'bots')
        # fields = ('id', 'username')
    
    def create(self, validated_data):
        
        user = User.objects.create_user(**validated_data)

        return user


class BehaviourSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    bot = serializers.ReadOnlyField(source='bot.id')
    active = serializers.BooleanField()
    type_behaviour = serializers.ChoiceField(choices=BEHAVIOUR_TYPES_CHOICES, required=False)
    
    class Meta:
        model = Behaviour
        fields = ('id', 'active', 'type_behaviour')

    def create(self, validated_data):
        """
        Create and return a new `Behaviour` instance, given the validated data.
        """
        if not 'type_behaviour' in validated_data:
            error_dict = dict()
            error_dict['type_behaviour'] = list()
            error_dict['type_behaviour'].append('This field is required.')
            raise ValidationError(error_dict)

        return Behaviour.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Behaviour` instance, given the validated data.
        """
        instance.active = validated_data.get('active', instance.active)
        instance.type_behaviour = validated_data.get('type_behaviour', instance.type_behaviour)
        instance.save()
        return instance


class TriggerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    behaviour = serializers.StringRelatedField(read_only=True, source='behaviour.id')
    word_trigger = serializers.CharField(required=True, max_length=100)
    type_trigger = serializers.ChoiceField(choices=TRIGGERS_CHOICES, required=False)

    def create(self, validated_data):
        """
        Create and return a new `Trigger` instance, given the validated data.
        """
        if not 'type_trigger' in validated_data:
            error_dict = dict()
            error_dict['type_trigger'] = list()
            error_dict['type_trigger'].append('This field is required.')
            raise ValidationError(error_dict)
        return Trigger.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Trigger` instance, given the validated data.
        """
        instance.word_trigger = validated_data.get('word_trigger', instance.word_trigger)
        instance.type_trigger = validated_data.get('type_trigger', instance.type_trigger)
        instance.save()
        return instance


class ReplySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    reply = serializers.CharField(required=True, max_length=200)

    def create(self, validated_data):
        """
        Create and return a new `Reply` instance, given the validated data.
        """
        return Reply.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Reply` instance, given the validated data.
        """
        instance.reply = validated_data.get('reply', instance.reply)
        instance.save()
        return instance
