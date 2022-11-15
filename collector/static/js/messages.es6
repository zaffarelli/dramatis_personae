let socket = new WebSocket(`ws://${window.location.host}/websocket/collector/`)
socket.onmessage = function (e) {
    console.log(e);
    let payload = JSON.parse(e.data);
    console.log(payload);
    console.log(payload['data']);
    $('#messenger_block').html(payload['data']);
    // $('.mosaic').innerHTML = payload;
}
