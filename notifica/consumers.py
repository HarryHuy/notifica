from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group, Channel
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.message import Message
import gc
from .classes import BaseManager

logged_users = BaseManager('logged_in', 'users')


@channel_session_user_from_http
def ws_add(message):
    if not message.user.is_authenticated:
        message.reply_channel.send({'accept': False})
    else:
        message.reply_channel.send({'accept': True, 'text': 'ws connection successful'})
        Group('notify-%s' % message.user.id).add(message.reply_channel)
        logged_users.add(message.user)


@channel_session_user
def ws_disconnect(message):
    message.reply_channel.send({'text': 'ws disconnected'})
    Group('notify-%s' % message.user.id).discard(message.reply_channel)
    logged_users.delete(message.user)


@channel_session_user
def ws_message(message):
    message.reply_channel.send({'text': 'message recieved'})


def ws_manual(message):
    Group('notify').send({'text': 'radiocheck'})


def ws_send_notify(message):
    if logged_users.get(message.text['recipient_id']):
        Group('notyfi-%s' % message.text['recipient_id'])\
            .send({'text': message.text})
