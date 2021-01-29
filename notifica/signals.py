from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth import user_logged_in, user_logged_out

from .models import Notify
from project.models import ExtendedUser


@receiver(post_save, sender=Notify)
def new_notify(sender, **kargs):
    if kargs['created'] is True:
        message = {
            'creator': kargs['instance'].creator.username,
            'recipient': kargs['instance'].recipient.username,
            'state': kargs['instance'].state,
            'type': kargs['instance'].type,
            'url': kargs['instance'].url
        }
        Channel('notify').send({'text': message})


@receiver(m2m_changed, sender=ExtendedUser.org.through)
def organization_changed(sender, **kwargs):
    if kwargs['action'] in ('post_add', 'post_remove'):
        instance = kwargs['instance']
        notify = Notify.objects.create(
            recipient=instance,
            creator=ExtendedUser.objects.get(pk=instance['creator_id']),
            state='unread',
            type=kwargs['action'],
        )

