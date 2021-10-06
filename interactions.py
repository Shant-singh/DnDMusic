# contains the responses for post requests for data about active games/socket connections
from flask import session, request
from flask_socketio import join_room, leave_room, SocketIO
from models import *
from app import app
from functions import *

socketio = SocketIO(app)

@socketio.on('join')
def joinRoom(data):
    print(f'{Users.query.get(session["id"]).username} has joined room {data["code"]}')
    game = ActiveGames.query.filter_by(game_id=Game.query.filter_by(game_code=data['code']).first().id).first()
    active_users = eval(game.active_users)
    active_users.append((session['id'], request.sid))
    game.active_users = str(active_users)
    db.session.commit()
    join_room(data['code'])

@socketio.on('disconnect')
def leaveRoom():
    for game in ActiveGames.query.all():
        users = eval(game.active_users)
        for user in users:
            if user[1] == request.sid:
                code = Game.query.get(game.game_id).game_code
                print(f'{Users.query.get(session["id"]).username} has left room {code}')
                users.pop(users.index(user))
                game.active_users = str(users)
                db.session.commit()
                leave_room(code)
                return

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