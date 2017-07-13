from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from channels.binding.websockets import WebsocketBinding


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
    member = models.ManyToManyField(ExtendedUser)

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=30)
    host = models.ForeignKey(Org, on_delete=models.CASCADE)
    date = models.DateField()
    participate = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


class Notify(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notify_recipient')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notify_sender')
    state = ('read', 'unread')
    content = models.CharField(max_length=30)
    url = models.CharField(max_length=50)

    def __str__(self):
        return self.content

class Message(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='message_recipient')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='message_sender')
    state = ('read', 'unread', 'unseen')
    content = models.CharField(max_length=100)

    def __str__(self):
        return self.content

class NotifyBinding(WebsocketBinding):
    model = Notify
    stream = 'notify'
    fields = ['recipient', 'creator', 'state', 'content', 'url']

    # groups receiving data
    @classmethod
    def group_names(cls, *args, **kwargs):
        group = list()
        for notify in args:
            group.append('ws-group-%s' % notify.recipient.id)
        return group

    def has_permission(self, user, action, pk):
        return True

class MessageBinding(WebsocketBinding):
    model = Message
    stream = 'message'
    fields = ['recipient', 'creator', 'state', 'content']

    @classmethod
    def group_names(cls, *args, **kwargs):
        group = list()
        for message in args:
            group.append('demultiplex-%s' % message.recipient.id)
        return group
        return ['ws-group-%s' % message.recipient.id]

    def has_permission(self, user, action, pk):
        return True
