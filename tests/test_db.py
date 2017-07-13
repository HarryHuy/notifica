from channels.test import ChannelTestCase, Client

class MyTests(ChannelTestCase):

    def test_my_consumer(self):
        client = Client()
        client.send_and_consume('my_internal_channel', {'value': 'my_value'})
        self.assertEqual(client.receive(), {'all is': 'done'})