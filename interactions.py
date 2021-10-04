# contains the responses for post requests for data about active games/socket connections
from flask_socketio import join_room, leave_room, SocketIO
from models import *
from app import app

socketio = SocketIO(app)

@socketio.on('join')
def joinRoom(data):
    join_room(data['code'])

@socketio.on('leave')
def leaveRoom(data):
    leave_room(data['code'])


# runs when a client requests to get new data from the db
@socketio.on('refresh')
def refreshData(data):
    game = ActiveGames.query.filter_by(game_id=data['game_code']).first()
    mapI = MapInstance.query.get(game.map_instance)
    map = Map.query.get(mapI.map_id)
    users = [Users.query.get(i).username for i in eval(game.active_users)]
    entities = [EntityInstance.query.get(i) for i in eval(mapI.entities)]
    entityData = []
    for entity in entities:
        e = Entity.query.get(entity.entity_id)
        entityData.append({
            'name': entity.name,
            'bigimageb64': e.bigimageb64,
            'iconb64': e.iconb64,
            'size': e.size,
            'x': entity.x_coord,
            'y': entity.y_coord
        })
    socketio.send({
        'online_users': users,
        'map': {
            'name': mapI.name,
            'initiative': mapI.initiative,
            'entities': entityData,
            'b64': map.imageb64,
            'scale': map.scale,
            'offset': map.offset,
            'xsize': map.xsize,
            'ysize': map.ysize
        }
    }, to=data['game_code'])

# runs when a client wants to update data from the db
@socketio.on('update')
def updateData(data):
    pass