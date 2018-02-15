# Generated by Django 2.0 on 2018-02-14 17:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telegrambot', '0003_telegrambot_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegrambot',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bots', to=settings.AUTH_USER_MODEL),
        ),
    ]
