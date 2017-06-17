$('document').ready(function () {
    var ws_path =  "/stream/";
    console.log("Connecting to " + ws_path);

    var webSocketBridge = new channels.WebSocketBridge();
    webSocketBridge.connect(ws_path);
    webSocketBridge.listen();
    webSocketBridge.demultiplex('notify', function(payload, streamName) {
        console.log(payload, streamName)
    });
    webSocketBridge.demultiplex('message', function(payload, streamName) {
        console.log(payload, streamName)
    })

    // Helpful debugging
    webSocketBridge.socket.addEventListener('open', function() { console.log("Connected to notification socket"); });
    webSocketBridge.socket.addEventListener('close', function() { console.log("Disconnected to notification socket"); });
});