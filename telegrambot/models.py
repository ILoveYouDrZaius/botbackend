from django.db import models
from telegram.ext import Updater, CommandHandler
import telegram, threading

# def worker(bot):
#     i = 0
#     while i<9999:
#         updates = bot.get_updates()
#         bot.
#         telegram.bot.
#         for u in updates:
#             bot.send_message(chat_id=8852679, text='Hola')
#         i += 1

TYPE_TRIGGER_CHOICE = (
    (0, 'Starts with'),
    (1, 'Contains'),
    (2, 'Ends with')
)

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

class Telegrambot(models.Model):
    name = models.CharField(max_length=30)
    token = models.CharField(max_length=50)
    # bot = telegram.Bot()

    def __init__(self, token):
        self.token = token
        updater = Updater(self.token)
        # for behaviour in behaviour_list:
            # if behaviour.type == 1:
            #     updater.dispatcher.add_handler(CommandHandler(behaviour.word,
            #         lambda (bot, update): update.message.reply_text(
            #             'Hello {}'.format(update.message.from_user.first_name))))
            # elif behaviour.type == 2:
            #     ...
        updater.dispatcher.add_handler(CommandHandler('hello',
            (lambda bot, update: (update.message.reply_text(
                'Hello {}'.format(update.message.from_user.first_name))))))

        updater.start_polling()
        # updater.idle
        # bot = telegram.Bot(token=self.token)
        # if bot.get_me().is_bot:
        #     self.name = bot.get_me().first_name
        # else:
        #     raise Exception('Token no válido')
        # # t = threading.Thread(target=worker, name=self.name, args=(bot,))
        # # t.start()
        # # print([u.message.text for u in updates])
        # # t = threading.Thread(name=self.id)
        # updates = bot.get_updates()    
        # for u in updates:
        #     print(u)
            # bot.send_message(chat_id=8852679, text='Hola')

    def __str__(self):
        return self.name

# class Trigger(models.Model):
#     name = models.CharField(max_length=100)
#     type = models.Field
#     trigger = models.CharField(max_length=50)
    
#     def __str__(self):
#         return self.name