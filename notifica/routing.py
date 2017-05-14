from channels.routing import route
from notifica.consumers import ws_add, ws_message, ws_disconnect

channel_routing = [
    # route("http.request", "notifica.consumers.http_consumer"),
    route('websocket.connect', ws_add),
    route('websocket.receive', ws_message),
    # route('websocket.disconnect', ws_disconnect)
]
