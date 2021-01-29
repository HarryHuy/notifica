from django.db import models
from django.conf import settings


# Create your models here.


class Notify(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notify_recipient', \
        on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notify_sender', \
        on_delete=models.CASCADE)
    state = ('read', 'unread', 'unseen')
    type = models.CharField(max_length=30, blank=True)
    url = models.CharField(max_length=50, blank=True)
