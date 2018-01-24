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

TYPE_TRIGGER_CHOICE = (
    (0, 'Starts with'),
    (1, 'Contains'),
    (2, 'Ends with')
)

class Telegrambot(models.Model):
    name = models.CharField(max_length=30)
    token = models.CharField(max_length=50)

    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self.name

    def start(self):
        updater = Updater(self.token)
        # for behaviour in behaviour_list:
            # if behaviour.type == 1:
            #     updater.dispatcher.add_handler(CommandHandler(behaviour.word,
            #         lambda (bot, update): update.message.reply_text(
            #             'Hello {}'.format(update.message.from_user.first_name))))
            # elif behaviour.type == 2:
            #     ...
        # updater.dispatcher.add_handler(CommandHandler('hello', f_cond))
        filtro = FilterContains()
        filtro.set_word('hola')
        
        updater.dispatcher.add_handler(MessageHandler((Filters.text & filtro), lambda bot, update:(
            update.message.reply_text(
                'Eso es y será'
            )
        )))

        updater.start_polling(clean=True)
        updater.idle()

    def stop(self):
        updater = Updater(self.token)
        updater.stop()
