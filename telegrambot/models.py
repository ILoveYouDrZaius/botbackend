from django.db import models
from django.contrib.auth.models import User
from operator import and_
from functools import reduce
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
from telegram.error import InvalidToken
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bots')
    name = models.CharField(max_length=30)
    token = models.CharField(max_length=50, unique=True)
    active = models.BooleanField(default=False)
    
    updater = None

    @staticmethod
    def test_token(token):
        try:
            Updater(token)
            return True
        except InvalidToken:
            return False

    def __init__(self, *args, **kwargs):               
        super(Telegrambot, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.token

    def start(self):
        self.updater = Updater(self.token)
        behaviour_list = Behaviour.objects.filter(bot=self, active=True)
        
        for behaviour in behaviour_list:
            triggers = Trigger.objects.filter(behaviour=behaviour)
            replies = Reply.objects.filter(behaviour=behaviour)
            print(replies)
            all_filters = None
            for trigger in triggers:
                if behaviour.type_behaviour == AND:
                    if not all_filters:
                        all_filters = CustomFilter(trigger.word_trigger, trigger.type_trigger)
                    else:
                        all_filters = all_filters.__and__(CustomFilter(trigger.word_trigger, trigger.type_trigger))
                elif behaviour.type_behaviour == OR:
                    if not all_filters:
                        all_filters = CustomFilter(trigger.word_trigger, trigger.type_trigger)
                    else:
                        all_filters = all_filters.__or__(CustomFilter(trigger.word_trigger, trigger.type_trigger))
            self.updater.dispatcher.add_handler(MessageHandler(filters=all_filters,
                        callback = (lambda replies: (lambda bot, update:(
                            update.message.reply_text((((lambda replies:(random.choice(replies).reply))(replies)))))))(replies)
            ))

        self.updater.start_polling(clean=True)

    def stop(self):
        if self.updater:
            self.updater.stop()
            self.updater = None

    def is_connected(self):

        return self.updater is not None


class Behaviour(models.Model):

    bot = models.ForeignKey(Telegrambot, on_delete=models.CASCADE, related_name='behaviour_bot')

    active = models.BooleanField(default=False)
    type_behaviour = models.IntegerField(choices=BEHAVIOUR_TYPES_CHOICES)

    def __str__(self):
        return 'behaviour {id}'.format(id=self.id)
    
    def save(self, *args, **kwargs):
        
        bot = self.bot

        super(Behaviour, self).save(*args, **kwargs)

        bot.stop()
        bot.start()

    def delete(self, *args, **kwargs):
        
        bot = self.bot

        super(Behaviour, self).delete()

        bot.stop()
        bot.start()


class Trigger(models.Model):

    behaviour = models.ForeignKey(Behaviour, on_delete=models.CASCADE, related_name='trigger_behaviour')
    word_trigger = models.CharField(max_length=100)
    type_trigger = models.IntegerField(choices=TRIGGERS_CHOICES)

    def save(self, *args, **kwargs):
        
        bot = self.behaviour.bot

        super(Trigger, self).save(*args, **kwargs)

        bot.stop()
        bot.start()
    
    def delete(self, *args, **kwargs):
        
        bot = self.behaviour.bot

        super(Trigger, self).delete()

        bot.stop()
        bot.start()

class Reply(models.Model):

    behaviour = models.ForeignKey(Behaviour, on_delete=models.CASCADE, related_name='reply_behaviour')
    reply = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        
        bot = self.behaviour.bot

        super(Reply, self).save(*args, **kwargs)

        bot.stop()
        bot.start()
    
    def delete(self, *args, **kwargs):
        
        bot = self.behaviour.bot

        super(Reply, self).delete()

        bot.stop()
        bot.start()
