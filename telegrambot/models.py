from django.db import models
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
import telegram, threading, time


class FilterContains(BaseFilter):
    def __init__(self):
        word = ''

    def set_word(self, word):
        self.word = word

    def filter(self, message):
        return self.word in message.text

TRIGGER_TYPES = (
    (0, 'Starts with'),
    (1, 'Contains'),
    (2, 'Ends with'),
)

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
            print('Token {token} recibido'.format(token=token))

    def __str__(self):
        return self.token

    def start(self):
        self.updater = Updater(self.token)
        behaviour_list = Behaviour.objects.filter(bot=self)
        
        for behaviour in behaviour_list:
            triggers = Trigger.objects.filter(behaviour=behaviour)
            for trigger in triggers:
                replies = Reply.objects.filter(trigger=trigger)
                for reply in replies:
                    if behaviour.type_trigger == 1:
                        filtro = FilterContains()
                        filtro.set_word(trigger.word_trigger)
                        self.updater.dispatcher.add_handler(MessageHandler((Filters.text & filtro), (lambda reply=reply: (lambda bot, update:(
                            update.message.reply_text(reply.reply))))(reply)
                            ))

        self.updater.start_polling(clean=True)
        self.updater.idle()

    def stop(self):
        self.updater.stop()

class Behaviour(models.Model):
    bot = models.ForeignKey(Telegrambot, on_delete=models.CASCADE, related_name='behaviour_bot')

    type_trigger = models.IntegerField(choices=TRIGGER_TYPES)
    active = models.BooleanField(default=False)
    # class Meta:
    #     unique_together = (("trigger", "bot"),)

class Trigger(models.Model):
    word_trigger = models.CharField(max_length=100)
    command = models.BooleanField()
    behaviour = models.ForeignKey(Behaviour, on_delete=models.CASCADE, related_name='trigger_behaviour')

class Reply(models.Model):
    reply = models.CharField(max_length=200)
    trigger = models.ForeignKey(Trigger, on_delete=models.CASCADE, related_name='reply_trigger')

    
