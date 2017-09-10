from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Position(models.Model):
    name = models.CharField(max_length=30)
    permission = models.CharField(max_length=30, blank=True)
    description = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50, blank=True)


class ExtendedUser(AbstractUser):
    code = models.PositiveIntegerField(blank=True, null=True)
    position = models.ManyToManyField(Position)
    org = models.ManyToManyField(Organization)

    def __str__(self):
        return self.username


class Activity(models.Model):
    name = models.CharField(max_length=30)
    host = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date = models.DateField()
    participate = models.ManyToManyField(settings.AUTH_USER_MODEL)


class Notify(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notify_recipient')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notify_sender')
    state = ('read', 'unread', 'unseen')
    type = models.CharField(max_length=30, blank=True)
    url = models.CharField(max_length=50, blank=True)
