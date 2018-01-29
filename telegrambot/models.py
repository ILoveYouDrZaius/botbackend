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
        # for behaviour in behaviour_list:
            # if behaviour.type == 1:
            #     updater.dispatcher.add_handler(CommandHandler(behaviour.word,
            #         lambda (bot, update): update.message.reply_text(
            #             'Hello {}'.format(update.message.from_user.first_name))))
            # elif behaviour.type == 2:
            #     ...
        # updater.dispatcher.add_handler(CommandHandler('hello', f_cond))

        # filtro = FilterContains()
        # filtro.set_word('hola')
        
        # self.updater.dispatcher.add_handler(MessageHandler((Filters.text & filtro), lambda bot, update:(
        #     update.message.reply_text(
        #         'Eso es y será'
        #     )
        # )))

        # self.updater.start_polling(clean=True)
        # self.updater.idle()

    def stop(self):
        self.updater.stop()


class Trigger(models.Model):
    word_trigger = models.CharField()
    command = models.BooleanField()

class Reply(models.Model):
    reply = models.CharField()

class Behaviour(models.Model):
    trigger = models.OneToOneField(Telegrambot, on_delete=models.CASCADE)
    reply = models.ManyToManyField(Reply)
    bot = models.ForeignKey(Telegrambot, on_delete=models.CASCADE)

    type_trigger = models.IntegerField(choices=TRIGGER_TYPES)
    active = models.BooleanField(default=False)
