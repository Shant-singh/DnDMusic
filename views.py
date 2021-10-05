from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_sqlalchemy import inspect
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from models import *
from functions import *
from app import app

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
    # remove stale 'active_games'
    for game in ActiveGames.query.all():
        # if game is more than two days old
        ActiveGames.query.filter_by(id = game.id).delete()
        if seconds_since() - game.time_created > 60 * 60 * 24 * 2:
            ActiveGames.query.filter_by(id = game.id).delete()
        db.session.commit()

    user = Users.query.get(session['id'])
    if session.get('game'):
        session.pop('game')
    if request.method == 'POST':
        # create something in the db
        if 'game' in request.form:
            create_game(db, request.form, user)
        if 'entity' in request.form:
            create_entity(db, request.form, user)
        if 'map' in request.form:
            create_map(db, request.form, user)

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
    user = Users.query.get(session['id'])
    games = eval(user.game_ids)
    game = Game.query.filter_by(game_code=request.args.get('c')).first()
    if request.args.get('c'):
        if game is not None and game.id in games:
            session['game'] = game.id

            if ActiveGames.query.filter_by(game_id=game.id).first() is None:
                # if the game is not yet active, activate it
                db.session.add(ActiveGames(game_id=game.id, active_users=f'[user.id]', map_instance=0, time_created=seconds_since()))
            else:
                # the game is already active, add this user
                active = ActiveGames.query.filter_by(game_id=game.id).first()
                a_au = eval(active.active_users)
                a_au.append(user.id)
                active.active_users = str(a_au)
            db.session.commit()

            return redirect(url_for('room'))
    if not session.get('game'):
        return redirect(url_for('home'))

    game = Game.query.get(session['game'])
    # if the request is post
    if request.method == 'POST':
        # if the user has authority to create stuff (is the dm)
        if session['id'] == game.dm_id:
            if 'entity' in request.form:
                create_entity_instance(db, request.form, user, MapInstance.query.get(request.form['mapR']))
            if 'map' in request.form:
                create_map_instance(db, request.form, user, game)

    if game.dm_id == session['id']:
        print(f'Connected to the DM interface of {game.game_code}')
        entities = [Entity.query.get(i) for i in eval(user.entity_ids)]
        maps = [Map.query.get(i) for i in eval(user.map_ids)]
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