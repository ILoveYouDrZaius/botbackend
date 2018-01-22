import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'botbackend.settings'
django.setup()

from telegrambot.models import *

def main():
    bot = Telegrambot(token='483224181:AAEa3MOFXyTKbUXnGhyAX_ihlSr0SbUVP6M')


if __name__ == '__main__':
    main()