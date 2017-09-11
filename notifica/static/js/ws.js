$('document').ready(function () {
    var ws_path =  "/ws-stream/";
    console.log("Connecting to " + ws_path);

    var webSocketBridge = new channels.WebSocketBridge();
    webSocketBridge.connect(ws_path);
    webSocketBridge.listen();
    webSocketBridge.demultiplex('notify', function(payload, streamName) {
        console.log(payload, streamName);

        if (payload['action'] == 'create') {
            $('.dropdown-menu').append(
                $('<li role="presentation">'
                + '<input class="id-store" type="hidden" value="' + payload['pk'] + '">'
                +'<a href="#">'
                + payload['data']['creator'] + ' ' + payload['data']['content']
                +'<button class="close"><span aria-hidden="true">×</span></button></a></li>'),
            )
        }

        if (payload['action'] == 'update') {

        }

        if (payload['action'] == 'delete') {
            notify = $('.id-store').filter(function() { return this.value == payload['pk'] });
            notify.parents('li').remove();
        }
    });

    // Helpful debugging
    webSocketBridge.socket.addEventListener('open', function() { console.log("Connected to notification socket"); });
    webSocketBridge.socket.addEventListener('close', function() { console.log("Disconnected to notification socket"); });
});