from django.db import models
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
            # reply = return_random_reply(replies)
            for trigger in triggers:
                # TODO: no obtener así el trigger
                filtro = CustomFilter(trigger.word_trigger, behaviour.type_trigger)

            self.updater.dispatcher.add_handler(MessageHandler((Filters.text & filtro),
                            (lambda replies: (lambda bot, update:(
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

    type_trigger = models.IntegerField(choices=TRIGGERS_CHOICES)
    active = models.BooleanField(default=False)


class Trigger(models.Model):
    word_trigger = models.CharField(max_length=100)
    command = models.BooleanField()
    behaviour = models.ForeignKey(Behaviour, on_delete=models.CASCADE, related_name='trigger_behaviour')

class Reply(models.Model):
    reply = models.CharField(max_length=200)
    behaviour = models.ForeignKey(Behaviour, on_delete=models.CASCADE, related_name='reply_behaviour')

    
