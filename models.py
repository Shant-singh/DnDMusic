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
    hash = db.Column(db.String(10)) # hash of the name for id purposes
    bigimageb64 = db.Column(db.String(200000))
    iconb64 = db.Column(db.String(200000))
    size = db.Column(db.String(3)) # binary for the six sizes

class EntityInstance(db.Model):
    __tablename__ = 'EntityInstance'
    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, db.ForeignKey('Entity.id'), nullable=False)
    map_id = db.Column(db.Integer, db.ForeignKey('MapInstance.id'), nullable=False)
    x_coord = db.Column(db.Integer)
    y_coord = db.Column(db.Integer)

class Map(db.Model):
    __tablename__ = 'Map'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    imageb64 = db.Column(db.String(1000))
    scale = db.Column(db.Integer)
    offset = db.Column(db.Integer)
    xsize = db.Column(db.Integer)
    ysize = db.Column(db.Integer)

class MapInstance(db.Model):
    __tablename__ = 'MapInstance'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    game_id = db.Column(db.Integer, db.ForeignKey('Game.id'), nullable=False)
    map_id = db.Column(db.Integer, db.ForeignKey('Map.id'), nullable=False)
    entities = db.Column(db.String(1000)) # list of ids of entities on this map
    initiative = db.Column(db.String(100)) # ordered list of tuples (entitylist_id, initiative_roll)

class Game(db.Model):
    __tablename__ = 'Game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    dm_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    map_instance_ids = db.Column(db.String(1000)) # list of ids of map instances in this game
    player_ids = db.Column(db.String(10)) # list of ids of players
    game_code = db.Column(db.String(5))

if __name__ == '__main__':
    app = Flask(__name__)
    app.secret_key = 'nVTnu_Y8tEZ9h1Z5sLKSMWXMgG_781x1jr4jqu2qWlYm9SOB0Ff3xXyXYS_Xqc5IJTfnkdz4tSETqodVrmJAy7cAf3JtcpjYT0Cl4IQ29tnA5TEpPg4DiQYrUTYWVFeSo_N_gnFbtZQzZKZWeSeuku5rGUtj_YA6XJKxcs4ZQrd5fy6gNvFBcMiVrPAhxI2thdi5Um3IrCHJITr7kacKUPbcn_Otb4hDNRltyVGtmOJnGNwM_vGApQF7VrjoO_y0yJFe6jepfYEOayeCKustjoLvqBh4nbELsit06r_340kfLQQ0yJKcGNUU10xmuwNn79NC9MSjG7GPfDsiRV1PkIMoPmnOI8YI5FDXK2ejTxSY6jVpCphvEYYUnShR7m9FfLwVFU37zNRLtcfCW5ef942OxYtdEpcm5iUKt2TkwIOyjRtJDEciqlSaM15ziNhPh3bXVmsPjPUiETxBar9DGlb0TVVeoUV54FWkuU2LREMPKHSP2Gm4tgTyu7VpLPdschdoTCavLGZqvHA6IZaJBrOAQUd0tEW7qAHWG6CIKh68vyjWm9kaqPOIp3BijGXTmn_FhUZ7uoQk_mgv96Fu2uNaMM9pazumL0tOZ5LdvfrihUCYTKmjEsiYXWS_3ksriGhPn_bqibnfdcPMiRvagpmSN9njfOCB8ijluD_hc3FSGTKn4A_xtcDLS9BGyXdp4ysSldllTZXa0IbKd4EBWLnLGhoXsWOP8oMxY_vBnmpANlcfadTdAPJzlup1T2rizzmV6sQvZYcRzKR8xtWqJ65NhvwxpiMJV80n4jE6fx15YEJaDk9eIQJcCcOtV25rgxqCJBYIMldn7uSr1aC0ntBrl_bJXMlyZOJ3XP6zRayR7f8KI89JgT3U2un0kdQi5oMn0EdXr1phYeJhVO7u3xMYHscNtuQ48wV7h2XsSrL8W3e0pFFde6VMQcgoIw42wu5HzoY6tgIIy8bIBecKztu966SxxRfCmTnIv_Ddksl4vial_lNaFDENlYUTYD8p'
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app=app)

    db.create_all(app=app)