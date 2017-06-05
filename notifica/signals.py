from django.db.models.signals import post_save
from .models import Notify
from django.dispatch import receiver
from django.contrib.auth import user_logged_in, user_logged_out


@receiver(post_save, sender=Notify)
def new_notify(sender, **kargs):
    if kargs['created'] == True:
        message = {
            'creator': kargs['instance'].creator.username,
            'recipient': kargs['instance'].recipient.username,
            'state': kargs['instance'].state,
            'type': kargs['instance'].type,
            'url': kargs['instance'].url
        }
        Channel('notify').send({'text': message})



