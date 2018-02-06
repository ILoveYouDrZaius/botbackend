from django.db import models
from django.contrib.auth.models import User
from operator import and_
from functools import reduce
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
import telegram
import random, threading, time

CONTAINS = 0
STARTS_WITH = 1
ENDS_WITH = 2

TRIGGERS_CHOICES = (
    (CONTAINS, 'Contains'),
    (STARTS_WITH, 'Starts with'),
    (ENDS_WITH, 'Ends with'),
)

OR = 0
AND = 1

BEHAVIOUR_TYPES_CHOICES = (
    (AND, 'And'),
    (OR, 'Or'),
)

class CustomFilter(BaseFilter):
    def __init__(self, word, filter_type):
        self.word = word
        self.filter_type = filter_type

    def filter(self, message):
        if self.filter_type == CONTAINS:
            return self.word in message.text
        elif self.filter_type == STARTS_WITH:
            return message.text.startswith(self.word) 
        elif self.filter_type == ENDS_WITH:
            return message.text.endswith(self.word)

class Telegrambot(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='behaviour_bot')
    name = models.CharField(max_length=30)
    token = models.CharField(max_length=50, primary_key=True)
    active = models.BooleanField(default=False)
    
    updater = None

    def __init__(self, *args, **kwargs):
        token = kwargs.pop('token', None)
        super(Telegrambot, self).__init__(*args, **kwargs)
        if token is not None:
            self.token = token

    def __str__(self):
        return self.token

    def start(self):
        self.updater = Updater(self.token)
        behaviour_list = Behaviour.objects.filter(bot=self)
        
        for behaviour in behaviour_list:
            triggers = Trigger.objects.filter(behaviour=behaviour)
            replies = Reply.objects.filter(behaviour=behaviour)
            all_filters = Filters.text
            for trigger in triggers:
                if behaviour.type_behaviour == AND:
                    all_filters = all_filters.__and__(CustomFilter(trigger.word_trigger, trigger.type_trigger))
                elif behaviour.type_behaviour == OR:
                    all_filters = all_filters.__or__(CustomFilter(trigger.word_trigger, trigger.type_trigger))
            # print(all_filters)

            self.updater.dispatcher.add_handler(MessageHandler(filters=(all_filters),
                        callback = (lambda replies: (lambda bot, update:(
                            update.message.reply_text((((lambda replies:(random.choice(replies).reply))(replies)))))))(replies)
            ))
        print('Bot arrancado...')

        self.updater.start_polling(clean=True)
        # self.updater.idle()

    def stop(self):

        self.updater.stop()

    def removehandlers(self):

        if not self.updater:
            self.updater = Updater(self.token)
        for handler in self.updater.dispatcher.handlers:
            self.updater.dispatcher.remove_handler(handler)
    

class Behaviour(models.Model):
    bot = models.ForeignKey(Telegrambot, on_delete=models.CASCADE, related_name='behaviour_bot')

    active = models.BooleanField(default=False)
    type_behaviour = models.IntegerField(choices=BEHAVIOUR_TYPES_CHOICES)

class Trigger(models.Model):
    word_trigger = models.CharField(max_length=100)
    command = models.BooleanField()
    type_trigger = models.IntegerField(choices=TRIGGERS_CHOICES)
    behaviour = models.ForeignKey(Behaviour, on_delete=models.CASCADE, related_name='trigger_behaviour')

class Reply(models.Model):
    reply = models.CharField(max_length=200)
    behaviour = models.ForeignKey(Behaviour, on_delete=models.CASCADE, related_name='reply_behaviour')

    
