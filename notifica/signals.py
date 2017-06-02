from django.db.models.signals import post_save
from .models import *
from django.dispatch import receiver
from django.contrib.auth import user_logged_in, user_logged_out
from .base import BaseManager


@receiver(post_save, sender=Org)
def activity_changed(sender, **kargs):
    print('Model has been changed!')

@receiver(user_logged_in)
def on_user_login(**kwargs):
    print('some one has logged in')
    user = kwargs.get('user')
    users = BaseManager('users_logged_in', 'users')
    users.add(user)
    print(users.count())
