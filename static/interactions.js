var socket = io();

socket.on('connect', function() {
    var game_code = document.querySelector('meta[name="game_code"]').content
    socket.emit('join', {'code': game_code});
});