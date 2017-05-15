from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    code = models.PositiveIntegerField(null=True)


class Position(models.Model):
    name = models.CharField(max_length=30)
    permission = models.CharField(max_length=30)
    descrip = models.CharField(max_length=50)


class Org(models.Model):
    name = models.CharField(max_length=30)
    descrip = models.CharField(max_length=50)


class Activity(models.Model):
    name = models.CharField(max_length=30)
    host = models.ForeignKey(Org, on_delete=models.CASCADE)
    date = models.DateField()
    # participate = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True)

    def __str__(self):
        return self.name


class Notify(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notify_recipient')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notify_sender')
    state = ('read', 'unread', 'unseen')
    type = models.CharField(max_length=30)
    reference = models.CharField(max_length=50)

