from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core import serializers
import json
from channels.binding.websockets import WebsocketBinding


class Position(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class ExtendedUser(AbstractUser):
    code = models.PositiveIntegerField(blank=True, null=True)
    position = models.ManyToManyField(Position, blank=True)
    org = models.ManyToManyField(Organization, blank=True)

    def __str__(self):
        return self.username

    def natural_key(self):
        return self.username


class Activity(models.Model):
    name = models.CharField(max_length=30)
    host = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date = models.DateField()
    participate = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


class Notify(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notify_recipient')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notify_sender')
    content = models.CharField(max_length=30)
    url = models.CharField(max_length=50)

    def __str__(self):
        return self.content


class Message(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='message_recipient')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='message_sender')
    type = models.CharField(max_length=30, blank=True)
    url = models.CharField(max_length=50, blank=True)
    content = models.CharField(max_length=100)

    def __str__(self):
        return self.content


class NotifyBinding(WebsocketBinding):
    model = Notify
    stream = 'notify'
    # fields = ['recipient', 'creator', 'content', 'url']
    fields = ['__all__']

    # groups receiving data
    @classmethod
    def group_names(cls, *args, **kwargs):
        group = list()
        for notify in args:
            group.append('ws-group-%s' % notify.recipient.id)
        return group

    def has_permission(self, user, action, pk):
        return True

    def serialize_data(self, instance):
        """
        Serializes model data into JSON-compatible types.
        """
        if self.fields is not None:
            if self.fields == '__all__' or list(self.fields) == ['__all__']:
                fields = None
            else:
                fields = self.fields
        else:
            fields = [f.name for f in instance._meta.get_fields() if f.name not in self.exclude]
        data = serializers.serialize(
            'json',
            [instance],
            fields=fields,
            use_natural_foreign_keys=True,
        )
        return json.loads(data)[0]['fields']


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
