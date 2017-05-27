from channels.routing import route
import notifica.consumers as csm

channel_routing = [
    # route("http.request", "notifica.consumers.http_consumer"),
    route('websocket.connect', csm.ws_add),
    route('websocket.receive', csm.ws_message),
    route('websocket.disconnect', csm.ws_disconnect),
    route('notify', csm.ws_manual)
]
