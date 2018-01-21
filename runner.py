import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "botbackend.settings")

from telegrambot.models import *

def main():
    print(Telegrambot.objects.all())

if __name__ == "__main__":
    main()