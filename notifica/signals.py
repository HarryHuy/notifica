from django.db.models.signals import post_save, pre_save, m2m_changed
from .models import *
from django.dispatch import receiver
from django.contrib.auth import user_logged_in, user_logged_out


UserModel = ExtendedUser


# @receiver(post_save, sender=ExtendedUser)
def user_changed(*args, **kwargs):
    if not kwargs['created']:
        notify = Notify()
        try:
            notify.creator = ExtendedUser.objects.get(id=kwargs['instance'].updated_by)
            notify.recipient = ExtendedUser.objects.get(id=kwargs['instance'].id)
        except ExtendedUser.DoesNotExist:
            print("Notify's user error")
        except AttributeError:
            print('Wrong update')
        else:
            notify.state = 'unread'
            notify.type = 'Your information has been changed by %s' % notify.creator
            notify.url = 'none'
            notify.save()


@receiver(m2m_changed, sender=UserModel.org.through)
def signal_org_change(**kwargs):
    pass
