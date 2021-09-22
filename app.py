from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy, inspect#, table_object
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from logging import Formatter, FileHandler
import os
from functools import wraps

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    game_ids = db.Column(db.String(100))
    permissions = db.Column(db.Integer) # ORed permissions 0x1 is admin

class Entity(db.Model):
    __tablename__ = 'Entity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    hash = db.Column(db.String(100)) # hash of the name for id purposes
    visibility = db.Column(db.String(1000))
    imageb64 = db.Column(db.String(1000))
    size = db.Column(db.String(50))

class EntityList(db.Model):
    __tablename__ = 'EntityList'
    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, db.ForeignKey('Entity.id'), nullable=False)
    map_id = db.Column(db.Integer, db.ForeignKey('MapInstance.id'), nullable=False)
    x_coord = db.Column(db.Integer)
    y_coord = db.Column(db.Integer)

class Map(db.Model):
    __tablename__ = 'Map'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    visibility = db.Column(db.String(1000))
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
    name = db.Column(db.String(100))
    visibility = db.Column(db.String(1000))
    dm_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    map_ids = db.Column(db.String(1000)) # list of ids of map instances in this game
    player_ids = db.Column(db.String(10)) # list of ids of players
    game_code = db.Column(db.String(20))

app = Flask(__name__)
app.secret_key = 'nVTnu_Y8tEZ9h1Z5sLKSMWXMgG_781x1jr4jqu2qWlYm9SOB0Ff3xXyXYS_Xqc5IJTfnkdz4tSETqodVrmJAy7cAf3JtcpjYT0Cl4IQ29tnA5TEpPg4DiQYrUTYWVFeSo_N_gnFbtZQzZKZWeSeuku5rGUtj_YA6XJKxcs4ZQrd5fy6gNvFBcMiVrPAhxI2thdi5Um3IrCHJITr7kacKUPbcn_Otb4hDNRltyVGtmOJnGNwM_vGApQF7VrjoO_y0yJFe6jepfYEOayeCKustjoLvqBh4nbELsit06r_340kfLQQ0yJKcGNUU10xmuwNn79NC9MSjG7GPfDsiRV1PkIMoPmnOI8YI5FDXK2ejTxSY6jVpCphvEYYUnShR7m9FfLwVFU37zNRLtcfCW5ef942OxYtdEpcm5iUKt2TkwIOyjRtJDEciqlSaM15ziNhPh3bXVmsPjPUiETxBar9DGlb0TVVeoUV54FWkuU2LREMPKHSP2Gm4tgTyu7VpLPdschdoTCavLGZqvHA6IZaJBrOAQUd0tEW7qAHWG6CIKh68vyjWm9kaqPOIp3BijGXTmn_FhUZ7uoQk_mgv96Fu2uNaMM9pazumL0tOZ5LdvfrihUCYTKmjEsiYXWS_3ksriGhPn_bqibnfdcPMiRvagpmSN9njfOCB8ijluD_hc3FSGTKn4A_xtcDLS9BGyXdp4ysSldllTZXa0IbKd4EBWLnLGhoXsWOP8oMxY_vBnmpANlcfadTdAPJzlup1T2rizzmV6sQvZYcRzKR8xtWqJ65NhvwxpiMJV80n4jE6fx15YEJaDk9eIQJcCcOtV25rgxqCJBYIMldn7uSr1aC0ntBrl_bJXMlyZOJ3XP6zRayR7f8KI89JgT3U2un0kdQi5oMn0EdXr1phYeJhVO7u3xMYHscNtuQ48wV7h2XsSrL8W3e0pFFde6VMQcgoIw42wu5HzoY6tgIIy8bIBecKztu966SxxRfCmTnIv_Ddksl4vial_lNaFDENlYUTYD8p'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app=app)

db.create_all(app=app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('id') or Users.query.get(session['id']) is None:
            return abort(403, "login_required")
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('id') or not Users.query.get(session['id']).permissions and 0x1:
            return abort(403, "admin_required")
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def home():
    game_ids = eval(Users.query.get(session['id']).game_ids)
    games = [Game.query.get(i) for i in game_ids]
    return render_template('index.html', games=games)

@app.route('/room')
def room():
    return render_template('room.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['uname'] == Users.query.filter_by(username=request.form['uname']).first().username and check_password_hash(Users.query.filter_by(username=request.form['uname']).first().password, request.form['psw']):
            session['id'] = Users.query.filter_by(username=request.form['uname']).first().id
            print(f'User {request.form["uname"]} logged in')
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    if session.get('id'):
        session.pop('id')
    return render_template('logout.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if not Users.query.filter_by(username=request.form['uname']).first():
            db.session.add(Users(username=request.form['uname'], password=generate_password_hash(request.form['psw']), game_ids='[1]', permissions=0x1))
            db.session.add(Game(name="Test Game", dm_id=0, game_code="XW95Y"))
            db.session.commit()
            print(f'Added user {request.form["uname"]} with password {request.form["psw"]}')
            return redirect(url_for('login'), code=303)
        else:
            print('No user added')
    return render_template('register.html')

@app.route('/admin')
@admin_required
def admin():
    inspector = inspect(db.engine)
    tables = db.Model.__subclasses__()
    data = {}
    for table in tables:
        data[table.__tablename__] = [[]]
        for column in inspector.get_columns(table.__tablename__):
            data[table.__tablename__][0].append(column['name'])
        data[table.__tablename__] += table.query.all()
    return render_template('admin.html', tables=data)

# Error handlers
@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def permission_error(error):
    return render_template('errors/403.html', error=error.description), 403

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)