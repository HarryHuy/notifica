from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Position(models.Model):
    name = models.CharField(max_length=30)
    # permission = models.CharField(max_length=30)
    description = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class ExtendedUser(AbstractUser):
    code = models.PositiveIntegerField(null=True)
    position = models.ForeignKey(Position, null=True)

    def __str__(self):
        return self.username


class Org(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50)


class Activity(models.Model):
    name = models.CharField(max_length=30)
    host = models.ForeignKey(Org, on_delete=models.CASCADE)
    date = models.DateField()
    participate = models.ManyToManyField(settings.AUTH_USER_MODEL)


class Notify(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notify_recipient')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notify_sender')
    state = ('read', 'unread', 'unseen')
    type = models.CharField(max_length=30)
    url = models.CharField(max_length=50)

