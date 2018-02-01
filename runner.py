import os, time
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'botbackend.settings'
django.setup()

from telegrambot.models import *

# def f(x):
#     return(lambda x: x + 5)


def main():
    bot = Telegrambot(token='483224181:AAEa3MOFXyTKbUXnGhyAX_ihlSr0SbUVP6M')
    bot.save()
    behaviour = Behaviour(type_trigger=1, active=True, bot=bot)
    behaviour.save()
    t = Trigger(word_trigger='ey', command=False, behaviour=behaviour)
    t.save()
    reply = Reply(reply='1', trigger=t)
    reply.save()
    behaviour2 = Behaviour(type_trigger=1, active=True, bot=bot)
    behaviour2.save()
    t2 = Trigger(word_trigger='ay', command=False, behaviour=behaviour2)
    t2.save()
    reply2 = Reply(reply='2', trigger=t2)
    reply2.save()
    bot.start()
    
    time.sleep(5)
    print('Parando...')
    bot.stop()
    time.sleep(2)
    print('Arrancando...')
    bot = Telegrambot(token='483224181:AAEa3MOFXyTKbUXnGhyAX_ihlSr0SbUVP6M')
    bot.removehandlers()
    bot.save()
    bot.start()

    Telegrambot.objects.all().delete()



if __name__ == '__main__':
    main()