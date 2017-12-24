from django.db import models

# Create your models here.

class Telegrambot(models.Model):
    name = models.CharField(max_length=30)
    token = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

    def start_bot(self):
        pass

class Trigger(models.Model):
    name = models.CharField(max_length=100)
    trigger = models.CharField(max_length=50)
    response = models.CharField(max_length=200)
    telegrambot = models.ForeignKey(Telegrambot, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name