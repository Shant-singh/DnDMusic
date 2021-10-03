from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_sqlalchemy import inspect
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from logging import Formatter, FileHandler
import os
from functools import wraps

from functions import *
from models import *

app = Flask(__name__)
app.secret_key = 'nVTnu_Y8tEZ9h1Z5sLKSMWXMgG_781x1jr4jqu2qWlYm9SOB0Ff3xXyXYS_Xqc5IJTfnkdz4tSETqodVrmJAy7cAf3JtcpjYT0Cl4IQ29tnA5TEpPg4DiQYrUTYWVFeSo_N_gnFbtZQzZKZWeSeuku5rGUtj_YA6XJKxcs4ZQrd5fy6gNvFBcMiVrPAhxI2thdi5Um3IrCHJITr7kacKUPbcn_Otb4hDNRltyVGtmOJnGNwM_vGApQF7VrjoO_y0yJFe6jepfYEOayeCKustjoLvqBh4nbELsit06r_340kfLQQ0yJKcGNUU10xmuwNn79NC9MSjG7GPfDsiRV1PkIMoPmnOI8YI5FDXK2ejTxSY6jVpCphvEYYUnShR7m9FfLwVFU37zNRLtcfCW5ef942OxYtdEpcm5iUKt2TkwIOyjRtJDEciqlSaM15ziNhPh3bXVmsPjPUiETxBar9DGlb0TVVeoUV54FWkuU2LREMPKHSP2Gm4tgTyu7VpLPdschdoTCavLGZqvHA6IZaJBrOAQUd0tEW7qAHWG6CIKh68vyjWm9kaqPOIp3BijGXTmn_FhUZ7uoQk_mgv96Fu2uNaMM9pazumL0tOZ5LdvfrihUCYTKmjEsiYXWS_3ksriGhPn_bqibnfdcPMiRvagpmSN9njfOCB8ijluD_hc3FSGTKn4A_xtcDLS9BGyXdp4ysSldllTZXa0IbKd4EBWLnLGhoXsWOP8oMxY_vBnmpANlcfadTdAPJzlup1T2rizzmV6sQvZYcRzKR8xtWqJ65NhvwxpiMJV80n4jE6fx15YEJaDk9eIQJcCcOtV25rgxqCJBYIMldn7uSr1aC0ntBrl_bJXMlyZOJ3XP6zRayR7f8KI89JgT3U2un0kdQi5oMn0EdXr1phYeJhVO7u3xMYHscNtuQ48wV7h2XsSrL8W3e0pFFde6VMQcgoIw42wu5HzoY6tgIIy8bIBecKztu966SxxRfCmTnIv_Ddksl4vial_lNaFDENlYUTYD8p'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app=app)
migrate = Migrate(app, db)

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
        try:
            if not session.get('id') or not (Users.query.get(session['id']).permissions and 0x1):
                return abort(403, "admin_required")
        except AttributeError: # the user has an invalid session id
            return redirect(url_for('logout'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if session.get('game'):
        session.pop('game')
    if request.method == 'POST':
        # create something in the db
        if 'game' in request.form:
            create_game(db, request.form, Users.query.get(session['id']))
        if 'entity' in request.form:
            create_entity(db, request.form, Users.query.get(session['id']))
        if 'map' in request.form:
            create_map(db, request.form, Users.query.get(session['id']))

    user = Users.query.get(session['id'])
    game_ids = eval(user.game_ids)
    map_ids = eval(user.map_ids)
    entity_ids = eval(user.entity_ids)
    games = [Game.query.get(i) for i in game_ids]
    maps = [Map.query.get(i) for i in map_ids]
    entities = [Entity.query.get(i) for i in entity_ids]
    return render_template('index.html', user=user, games=games, maps=maps, entities=entities)

@app.route('/room', methods=['GET', 'POST'])
@login_required
def room():
    games = eval(Users.query.get(session['id']).game_ids)
    game = Game.query.filter_by(game_code=request.args.get('c')).first()
    if request.args.get('c'):
        if game is not None and game.id in games:
            session['game'] = game.id
            return redirect(url_for('room'))
    if not session.get('game'):
        return redirect(url_for('home'))

    game = Game.query.get(session['game'])
    # if the request is post
    if request.method == 'POST':
        # if the user has authority to create stuff (dm)
        if session['id'] == game.dm_id:
            if 'entity' in request.form:
                create_entity_instance(db, request.form, Users.query.get(session['id']), MapInstance.query.get(request.form['mapR']))
            if 'map' in request.form:
                create_map_instance(db, request.form, Users.query.get(session['id']), game)

    if game.dm_id == session['id']:
        print(f'Connected to the DM interface of {game.game_code}')
        entities = [Entity.query.get(i) for i in eval(Users.query.get(session['id']).entity_ids)]
        maps = [Map.query.get(i) for i in eval(Users.query.get(session['id']).map_ids)]
        mapInstances = [MapInstance.query.get(i) for i in eval(Game.query.get(session['game']).map_instance_ids)]
        return render_template('dm.html', entities=entities, maps=maps, mapInstances=mapInstances)
    print(f'Connected to the player interface of {game.game_code}')
    return render_template('room.html')

@app.route('/edit')
@login_required
def edit():
    return render_template('edit.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['uname'] == Users.query.filter_by(username=request.form['uname']).first().username and check_password_hash(Users.query.filter_by(username=request.form['uname']).first().password, request.form['psw']):
            session['id'] = Users.query.filter_by(username=request.form['uname']).first().id
            print(f'User {request.form["uname"]} logged in')
            return redirect(url_for('home'), code=303)
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
            db.session.add(Users(username=request.form['uname'], password=generate_password_hash(request.form['psw']), game_ids='[]', map_ids='[]', entity_ids='[]', permissions=0x1))
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
    app.run(host='0.0.0.0', port=80, debug=True, use_reloader=True)