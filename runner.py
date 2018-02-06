import os, time
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'botbackend.settings'
django.setup()

from telegrambot.models import *

# def f(x):
#     return(lambda x: x + 5)


def main():
    Telegrambot.objects.all().delete()
    Trigger.objects.all().delete()
    Reply.objects.all().delete()
    Behaviour.objects.all().delete()

    bot = Telegrambot(token='483224181:AAEa3MOFXyTKbUXnGhyAX_ihlSr0SbUVP6M')
    bot.save()
    behaviour = Behaviour(type_behaviour=0, active=True, bot=bot)
    behaviour.save()

    t = Trigger(type_trigger=0, word_trigger='ey', command=False, behaviour=behaviour)
    t.save()
    t2 = Trigger(type_trigger=0, word_trigger='oy', command=False, behaviour=behaviour)
    t2.save()
    reply = Reply(reply='1', behaviour=behaviour)
    reply.save()

    reply2 = Reply(reply='OJOOOO', behaviour=behaviour)
    reply2.save()

    behaviour2 = Behaviour(type_behaviour=1, active=True, bot=bot)
    behaviour2.save()

    t4 = Trigger(type_trigger=0, word_trigger='ay', command=False, behaviour=behaviour2)
    t4.save()
    t5 = Trigger(type_trigger=0, word_trigger='uy', command=False, behaviour=behaviour2)
    t5.save()
    reply4 = Reply(reply='124', behaviour=behaviour2)
    reply4.save()
    bot.start()
    # time.sleep(5)
    # print('Parando...')
    # bot.stop()
    # time.sleep(2)
    # print('Arrancando...')
    # bot = Telegrambot(token='483224181:AAEa3MOFXyTKbUXnGhyAX_ihlSr0SbUVP6M')
    # bot.removehandlers()
    # bot.save()
    # bot.start()

    # Telegrambot.objects.all().delete()



if __name__ == '__main__':
    main()