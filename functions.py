from datetime import datetime
import hashlib
import base64

from models import *

def generate_hash(string, length=10):
    return base64.urlsafe_b64encode(hashlib.sha1((string + str(datetime.now())).encode('utf8')).digest()).decode('utf8')[:length]

def seconds_since() -> float:
    # returns number of seconds since 00:00 01/01/2021
    return (datetime.now()-datetime(2021,1,1)).total_seconds()

def create_game(db, form, user):
    hash = generate_hash(form['name'], 5)
    db.session.add(Game(name=f"{form['name'][:100]}", dm_id=user.id, game_code=f"{hash}", map_instance_ids='[]', player_ids='[]'))
    game_ids = eval(user.game_ids)
    game_ids.append(Game.query.filter_by(game_code=hash).first().id)
    user.game_ids = str(game_ids)
    db.session.commit()

def create_entity(db, form, user):
    hash = generate_hash(form['name'], 10)
    db.session.add(Entity(name=f"{form['name'][:100]}", hash=f"{hash}", bigimageb64=f"{form['entityImageB']}", iconb64=f"{form['entityIconB']}", size=form['sizes']))
    entity_ids = eval(user.entity_ids)
    entity_ids.append(Entity.query.filter_by(hash=hash).first().id)
    user.entity_ids = str(entity_ids)
    db.session.commit()    

def create_map(db, form, user):
    hash = generate_hash(form['name'], 10)
    db.session.add(Map(name=f"{form['name'][:100]}", hash=f"{hash}", imageb64=f"{form['mapImageB']}", xcount=60, ycount=80))
    map_ids = eval(user.map_ids)
    map_ids.append(Map.query.filter_by(hash=hash).first().id)
    user.map_ids = str(map_ids)
    db.session.commit()
    
def create_map_instance(db, form, user, game):
    hash = generate_hash(form['name'], 10)
    db.session.add(MapInstance(name=f"{form['name'][:100]}", hash=hash, game_id=game.id, map_id=f"{form['mapSelect']}", entities=f"[]", initiative=f"[()]"))
    map_instance_ids = eval(game.map_instance_ids)
    map_instance_ids.append(MapInstance.query.filter_by(hash=hash).first().id)
    game.map_instance_ids = str(map_instance_ids)
    db.session.commit()
    
def create_entity_instance(db, form, user, map):
    hash = generate_hash(form['name'], 10)
    db.session.add(EntityInstance(name=f"{form['name'][:100]}", hash=hash, entity_id=f"{form['entitySelect']}", map_id=map.id, x_coord=0, y_coord=0))
    entities = eval(map.entities)
    entities.append(EntityInstance.query.filter_by(hash=hash).first().id)
    map.entities = str(entities)
    db.session.commit()