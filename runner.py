import os, time
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'botbackend.settings'
django.setup()

from telegrambot.models import *


def main():
    for user in User.objects.all():
        if not user.is_superuser:
            user.delete()

    Telegrambot.objects.all().delete()
    Trigger.objects.all().delete()
    Reply.objects.all().delete()
    Behaviour.objects.all().delete()

    user = User.objects.create_user(username='Manolo', password='123456')

    bot = Telegrambot(token='483224181:AAEa3MOFXyTKbUXnGhyAX_ihlSr0SbUVP6M', user=user)
    bot.save()
    # print('Token: {t}'.format(t=bot.token))
    behaviour = Behaviour(type_behaviour=0, active=True, bot=bot)
    behaviour.save()

    t = Trigger(type_trigger=0, word_trigger='ey', behaviour=behaviour)
    t.save()
    t2 = Trigger(type_trigger=0, word_trigger='oy', behaviour=behaviour)
    t2.save()
    reply = Reply(reply='1', behaviour=behaviour)
    reply.save()

    reply2 = Reply(reply='OJOOOO', behaviour=behaviour)
    reply2.save()

    behaviour2 = Behaviour(type_behaviour=1, active=True, bot=bot)
    behaviour2.save()

    t4 = Trigger(type_trigger=0, word_trigger='ay', behaviour=behaviour2)
    t4.save()
    t5 = Trigger(type_trigger=0, word_trigger='uy', behaviour=behaviour2)
    t5.save()
    reply4 = Reply(reply='124', behaviour=behaviour2)
    reply4.save()
    print(bot.is_connected())
    # bot.start()
    print(bot.is_connected())
    
    # Telegrambot.objects.all().delete()



if __name__ == '__main__':
    main()