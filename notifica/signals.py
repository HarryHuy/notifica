from django.db.models.signals import post_save
from .models import *
from django.dispatch import receiver


@receiver(post_save, sender=Org)
def activity_changed(sender, **kargs):
    print('Model has been changed!')
