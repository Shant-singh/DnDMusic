var socket = io();

function game_code() {
    var game_code = document.querySelector('meta[name="game_code"]').content;
    return game_code;
}

socket.on('connect', function() {
    socket.emit('join', {'code': game_code()});
});

function drawCanvas (base64, xcount, ycount) {
    var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext("2d");

    var background = new Image();
    background.src = base64;
    
    background.onload = function(){
        canvas.width = background.width;
        canvas.height = background.height;
        ctx.drawImage(background, 0, 0, this.width, this.height);

        var width = background.width/xcount;
        var height = background.height/ycount;
        console.log(width, height)
        var data = '<svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg"> \
            <defs> \
                <pattern id="smallGrid" width="'+width+'" height="'+height+'" patternUnits="userSpaceOnUse"> \
                    <path d="M '+width+' 0 L 0 0 0 '+height+'" fill="none" stroke="black" stroke-width="2" /> \
                </pattern> \
            </defs> \
            <rect width="100%" height="100%" fill="url(#smallGrid)" /> \
        </svg>';

        var DOMURL = window.URL || window.webkitURL || window;
        var grid = new Image();
        var svg = new Blob([data], {type: 'image/svg+xml;charset=utf-8'});
        var url = DOMURL.createObjectURL(svg);
        grid.onload = function(){
            ctx.drawImage(grid, 0, 0);
            DOMURL.revokeObjectURL(url);
        }
        grid.src = url;
    }
    
}

socket.on("refresh", function(data) {
    drawCanvas(data['map']['b64'], data['map']['xcount'], data['map']['xcount']);
    console.log('refreshed');
});

window.onload = function(){
    socket.emit('refresh', {'game_code': game_code()});
}