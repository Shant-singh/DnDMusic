from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    game_ids = db.Column(db.String(100))
    map_ids = db.Column(db.String(100))
    entity_ids = db.Column(db.String(100))
    permissions = db.Column(db.Integer) # ORed permissions, 0x1 is admin

class Entity(db.Model):
    __tablename__ = 'Entity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    hash = db.Column(db.String(10), unique=True) # hash of the name for id purposes
    bigimageb64 = db.Column(db.String(200000))
    iconb64 = db.Column(db.String(200000))
    size = db.Column(db.String(3)) # binary values for the different six sizes

class EntityInstance(db.Model):
    __tablename__ = 'EntityInstance'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    hash = db.Column(db.String(10), unique=True)
    entity_id = db.Column(db.Integer, db.ForeignKey('Entity.id'), nullable=False)
    map_id = db.Column(db.Integer, db.ForeignKey('MapInstance.id'), nullable=False)
    x_coord = db.Column(db.Integer)
    y_coord = db.Column(db.Integer)

class Map(db.Model):
    __tablename__ = 'Map'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    hash = db.Column(db.String(10), unique=True)
    imageb64 = db.Column(db.String(200000))
    xcount = db.Column(db.Integer)
    ycount = db.Column(db.Integer)

class MapInstance(db.Model):
    __tablename__ = 'MapInstance'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    hash = db.Column(db.String(10), unique=True)
    game_id = db.Column(db.Integer, db.ForeignKey('Game.id'), nullable=False)
    map_id = db.Column(db.Integer, db.ForeignKey('Map.id'), nullable=False)
    entities = db.Column(db.String(1000)) # list of ids of entities on this map
    initiative = db.Column(db.String(100)) # ordered list of tuples (entitylist_id, initiative_roll)

class Game(db.Model):
    __tablename__ = 'Game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dm_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    map_instance_ids = db.Column(db.String(1000)) # list of ids of map instances in this game
    player_ids = db.Column(db.String(10)) # list of ids of players
    game_code = db.Column(db.String(5), unique=True)

class ActiveGames(db.Model):
    __tablename__ = 'ActiveGames'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('Game.id'), nullable=False)
    active_users = db.Column(db.String(200)) # [(user.id, user.sid)] user.sid is 20 characters
    map_instance = db.Column(db.Integer, db.ForeignKey('MapInstance.id'), nullable=False)
    time_created = db.Column(db.Float) # seconds since 00:00 1st Jan 2021
    delta = db.Column(db.String(1000)) # changes since last periodic refresh