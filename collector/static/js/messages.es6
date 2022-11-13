
console.log('Enabling messaging websocket...')
socket = new WebSocket('ws://localhost:8088/websocket/collector/')
socket.onmessage = function (e) {
    let djangoData = JSON.parse(e.data);
    console.log(djangoData);
}
