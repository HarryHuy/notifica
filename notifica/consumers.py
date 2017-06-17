from channels.generic.websockets import WebsocketDemultiplexer
from .models import NotifyBinding, MessageBinding
from .ultils import logged_users
from channels import Group

class Demultiplexer(WebsocketDemultiplexer):
    http_user = True
    http_user_and_session = True

    consumers = {
        'notify': NotifyBinding.consumer,
        'message': MessageBinding.consumer
    }

    groups = ['demultiplex']

    # group name with user's id wrapped
    def raw_connect(self, message, **kwargs):
        for group in self.connection_groups(**kwargs):
            Group(group + str('-%s' % message.user.id),
                  channel_layer=message.channel_layer).add(message.reply_channel)
        self.connect(message, **kwargs)