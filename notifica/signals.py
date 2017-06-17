from django.db.models.signals import post_save
from .models import Notify
from django.dispatch import receiver
from django.contrib.auth import user_logged_in, user_logged_out



