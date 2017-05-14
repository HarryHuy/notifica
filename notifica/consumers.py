from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.message import Message
import gc


def http_consumer(message):
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)


@channel_session_user_from_http
def ws_add(message):
    if message.user.is_authenticated is False:
        message.reply_channel.send({'accept': False})
    else:
        message.reply_channel.send({'accept': True})
        # Group('chat').add(message.reply_channel)
        # print(dict(message.user))


@channel_session_user
def ws_disconnect(message):
    Group('chat').discard(message.reply_channel)


# @channel_session_user
# def ws_message(message):
#     print(message.user, message.reply_channel)
#     Group('chat').send({
#         'text': '[%s] %s' % (message.user, message['text'])
#     })


@channel_session_user
def ws_message(message):
    inst = [obj for obj in gc.get_referrers(Message) if isinstance(obj, Message)]
    for i in inst:
        if i.channel.name == 'websocket.connect':
            if i.user.username == 'harry':
                i.reply_channel.send({'text': message.content['text']})

