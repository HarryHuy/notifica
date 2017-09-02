from channels.generic.websockets import WebsocketDemultiplexer, JsonWebsocketConsumer
from .models import NotifyBinding, MessageBinding, ExtendedUser
from .ultils import logged_users
from channels import Group


class Demultiplexer(WebsocketDemultiplexer):
    http_user = True
    http_user_and_session = True

    consumers = {
        'notify': NotifyBinding.consumer,
        'message': MessageBinding.consumer
    }

    # grouping clients when connected
    groups = ['ws-group']

    # group name with userid combined
    def raw_connect(self, message, **kwargs):
        for group in self.connection_groups(**kwargs):
            Group(group + str('-%s' % message.user.id),
                  channel_layer=message.channel_layer).add(message.reply_channel)
        self.connect(message, **kwargs)

    def connect(self, message, **kwargs):
        """Forward connection to all consumers."""
        if self.message.user.is_authenticated:
            self.message.reply_channel.send({"accept": True})
        for stream, consumer in self.consumers.items():
            kwargs['multiplexer'] = self.multiplexer_class(stream, self.message.reply_channel)
            consumer(message, **kwargs)

