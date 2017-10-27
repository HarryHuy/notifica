from django.db.models.signals import post_save, m2m_changed
from .models import *
from django.dispatch import receiver
from django.contrib.auth import user_logged_in, user_logged_out


UserModel = ExtendedUser


# @receiver(post_save, sender=Notify)
def new_notify(sender, **kargs):
    if kargs['created'] is True:
        message = {
            'creator': kargs['instance'].creator.username,
            'recipient': kargs['instance'].recipient.username,
            'type': kargs['instance'].type,
            'url': kargs['instance'].url
        }
        Channel('notify').send({'text': message})


# @receiver(m2m_changed, sender=ExtendedUser.org.through)
def user_org_changed(sender, **kwargs):
    if kwargs['action'] in ('post_add', 'post_remove'):
        instance = kwargs['instance']
        # instance.creator hasn't been covered
        notify = Notify.objects.create(
            recipient=instance,
            creator=instance.creator,
            content=kwargs['action'],
        )
