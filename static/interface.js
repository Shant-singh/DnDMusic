var socket = io();

function game_code() {
    var game_code = document.querySelector('meta[name="game_code"]').content;
    return game_code;
}

socket.on('connect', function() {
    socket.emit('join', {'code': game_code()});
});

function drawEntity (entities, i, width, height, ycount) {
    var canvas = document.querySelector('canvas#e'+entities[i]['id']);
    if (canvas == null)
    {
        canvas = document.createElement('canvas');
        canvas.id = 'e'+entities[i]['id'];
        var map = document.querySelector('div.map');
        map.appendChild(canvas);
    }
    var ctx = canvas.getContext("2d");

    var image = new Image();
    image.src = entities[i]['iconb64']
    image.onload = function() {
        ctx.drawImage(image, 0, 0, width, height, width*entities[i]['x'], height*(ycount-entities[i]['y']-1), width, height);
    }
}

function drawCanvas (base64, xcount, ycount, entities) {
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
        var svgdata = '<svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg"> \
        <defs> \
        <pattern id="smallGrid" width="'+width+'" height="'+height+'" patternUnits="userSpaceOnUse"> \
        <path d="M '+width+' 0 L 0 0 0 '+height+'" fill="none" stroke="black" stroke-width="2" /> \
        </pattern> \
        </defs> \
        <rect width="100%" height="100%" fill="url(#smallGrid)" /> \
        </svg>';
        
        var DOMURL = window.URL || window.webkitURL || window;
        var grid = new Image();
        var svg = new Blob([svgdata], {type: 'image/svg+xml;charset=utf-8'});
        var url = DOMURL.createObjectURL(svg);
        grid.onload = function(){
            ctx.drawImage(grid, 0, 0);
            DOMURL.revokeObjectURL(url);
        }
        grid.src = url;

        // draw the entities
        for (var i = 0; i<entities.length; i++)
        {
            document.querySelectorAll('canvas[id^=\'e\']').forEach(e => e.remove()); // remove all entity canvases
            drawEntity(entities, i, width, height, ycount);
        }
    }
    
}

socket.on("refresh", function(data) {
    drawCanvas(data['map']['b64'], data['map']['xcount'], data['map']['ycount'], data['map']['entities']);

    mapInstances = document.querySelectorAll('div.mapInstance');
    for (var i=0; i<mapInstances.length; i++)
    {
        mapInstances[i].classList.remove('bold');
        if (data['map']['id'] == mapInstances[i].id)
        {
            mapInstances[i].classList.add('bold');
        }
        mapInstances[i].innerHTML = '<a href=\'#\' onclick="socket.emit(\'changeMap\', {\'game_code\': game_code(), \'map_id\': this.parentElement.id});">' + mapInstances[i].innerHTML + '</a>';
    }
});

window.addEventListener("load", function(){
    socket.emit('refresh', {'game_code': game_code()});
}, false);