from django.test import TestCase
from .models import Telegrambot
from django.contrib.auth.models import User
from telegram.error import InvalidToken

class TelegramBotTest(TestCase):

    def setUp(self):

        self.user = User(username='Manolo', password='123456')
        
    def test_create_valid_token(self):

        bot = Telegrambot(token='483224181:AAEa3MOFXyTKbUXnGhyAX_ihlSr0SbUVP6M', user=self.user)
        self.assertIsInstance(bot, Telegrambot)
    
    def test_create_wrong_token(self):

        bot = Telegrambot(token='zzzzz', user=self.user)
        self.assertIsInstance(bot, Telegrambot)

    def test_start_valid_token(self):

        bot = Telegrambot(token='483224181:AAEa3MOFXyTKbUXnGhyAX_ihlSr0SbUVP6M', user=self.user)
        bot.start()
        self.assertIsInstance(bot, Telegrambot)
        self.assertEqual(bot.is_connected(), True)

    def test_start_wrong_token(self):

        bot = Telegrambot(token='xxxxxxx', user=self.user)
        with self.assertRaises(InvalidToken):
            bot.start()
        self.assertEqual(bot.is_connected(), False)        

        

