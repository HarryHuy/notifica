from channels.routing import route_class, route
from .consumers import Demultiplexer
from notifica import consumers

channel_routing = [
    # route("http.request", "notifica.consumers.http_consumer"),
    # route('websocket.connect', consumers.ws_add),
    # route('websocket.receive', consumers.ws_message),
    # route('websocket.disconnect', consumers.ws_disconnect),
    # route('notify', consumers.ws_send_notify),
    route_class(Demultiplexer, path='^/ws-stream/?$')
]
