from django.db import models
from telegram.ext import Updater, CommandHandler
import telegram, threading

# Create your models here.

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

# def worker(bot):
#     i = 0
#     while i<9999:
#         updates = bot.get_updates()
#         bot.
#         telegram.bot.
#         for u in updates:
#             bot.send_message(chat_id=8852679, text='Hola')
#         i += 1

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
        updater.dispatcher.add_handler(CommandHandler('hello', hello))
        updater.start_polling()
        updater.idle
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

class Trigger(models.Model):
    name = models.CharField(max_length=100)
    trigger = models.CharField(max_length=50)
    response = models.CharField(max_length=200)
    telegrambot = models.ForeignKey(Telegrambot, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name