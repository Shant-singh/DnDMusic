# contains the responses for post requests for data about active games/socket connections
from flask import session, request
from flask_socketio import join_room, leave_room, SocketIO
from models import *
from app import app
from functions import *
import time

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
    game_id = Game.query.filter_by(game_code=data['game_code']).first().id
    game = ActiveGames.query.filter_by(game_id=game_id).first()
    mapI = MapInstance.query.get(game.map_instance)
    map = Map.query.get(mapI.map_id)
    users = [Users.query.get(i[0]).username for i in eval(game.active_users)]
    entities = [EntityInstance.query.get(i) for i in eval(mapI.entities)]
    entityData = []
    for entity in entities:
        e = Entity.query.get(entity.entity_id)
        entityData.append({
            'id': entity.id,
            'name': entity.name,
            'bigimageb64': e.bigimageb64,
            'iconb64': e.iconb64,
            'size': e.size,
            'x': entity.x_coord,
            'y': entity.y_coord
        })
    socketio.emit('refresh', {
        'online_users': users,
        'map': {
            'id': mapI.id,
            'name': mapI.name,
            'initiative': mapI.initiative,
            'entities': entityData,
            'b64': map.imageb64,
            'xcount': map.xcount,
            'ycount': map.ycount
        }
    }, room=data['game_code'])

# runs to tell the client the updated game data (delta)
@socketio.on('update')
def updateData(data):
    pass

@socketio.on('changeMap')
def changeMap(data):
    game = Game.query.filter_by(game_code=data['game_code']).first()
    active_game = ActiveGames.query.filter_by(game_id=game.id).first()
    user = Users.query.get(session['id'])
    if game.dm_id == user.id:
        if int(data['map_id']) in eval(game.map_instance_ids):
            print(f'{active_game.map_instance} into {int(data["map_id"])}')
            active_game.map_instance = int(data['map_id'])
            db.session.commit()
            refreshData(data) # get all clients to refresh their data (for the change in map)