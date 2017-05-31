from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group, Channel
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.message import Message
import gc


def http_consumer(message):
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)


@channel_session_user_from_http
def ws_add(message):
    # global channel_list
    channel_list = []
    # if message.user.is_authenticated is False:
    #     message.reply_channel.send({'accept': False})
    # else:
    #     message.reply_channel.send({'accept': True})
    #     Group('notify').add(message.reply_channel)
    message.reply_channel.send({'accept': True, 'text': 'ws connection successful'})
    # Group('notify').add(message.reply_channel)
    channel_list.append({'user': message.user,
                         'reply_channel': message.reply_channel})


@channel_session_user
def ws_disconnect(message):
    message.reply_channel.send({'text': 'ws disconnected'})
    Group('notify').discard(message.reply_channel)


@channel_session_user
def ws_message(message):
    # print(message.user, message.reply_channel)
    # Group('notify').send({
        # 'text': '[%s] %s' % (message.user, message['text'])
    # })
    message.reply_channel.send({'text': 'message recieved'})
    print(channel_list)
    # inst = [obj for obj in gc.get_referrers(Channel) if isinstance(obj, Channel)]
    # for i in inst:
        # print(i.__dict__)
    #     if i.channel.name == 'websocket.connect':
    #         if i.user.username == 'harry':
    #             i.reply_channel.send({'text': message.content['text']})

def ws_manual(message):
    group = Group('notify')
    group.send(message.content)

