import os, time
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'botbackend.settings'
django.setup()

from telegrambot.models import *

# def f(x):
#     return(lambda x: x + 5)


def main():
    bot = Telegrambot(token='483224181:AAEa3MOFXyTKbUXnGhyAX_ihlSr0SbUVP6M')
    # bot2 = Telegrambot(token='512586632:AAGnJzSgzNpL81ogn-91Q6TkMzyoHj9za_k')
    bot.start()
    # time.sleep(5)
    # bot.stop()
    # func = f(2)
    # print(func(2))


if __name__ == '__main__':
    main()