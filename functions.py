from datetime import datetime
import hashlib
import base64

from models import *

def generate_hash(string, length=10):
    return base64.urlsafe_b64encode(hashlib.sha1((string + str(datetime.now())).encode('utf8')).digest()).decode('utf8')[:length]

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
    db.session.add(Map(name=f"{form['name'][:100]}", hash=f"{hash}", imageb64=f"{form['mapImageB']}"))
    map_ids = eval(user.map_ids)
    map_ids.append(Map.query.filter_by(hash=hash).first().id)
    user.map_ids = str(map_ids)
    db.session.commit()