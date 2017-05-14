from django.db import models
from django.contrib.auth.models import User


class Position(models.Model):
    name = models.CharField(max_length=30)
    permission = models.CharField(max_length=30)
    descrip = models.CharField(max_length=50)


class Activity(models.Model):
    name = models.CharField(max_length=30)
    host = models.ForeignKey(Orgs, on_delete=models.CASCADE)
    date = models.DateField()
    participate = models.ManyToManyField(User, blank=True)


class Orgs(models.Model):
    name = models.CharField(max_length=30)
    descrip = models.CharField(max_length=50)


class Notifies(models.Model):
    recipient = models.ForeignKey(User)
    sender = models.ForeignKey(User)
    state = ('read', 'unread', 'unseen')
    type = models.CharField(max_length=30)
    reference = models.CharField(max_length=50)

