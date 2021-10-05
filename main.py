from app import app
from interactions import socketio

from errors import *
from views import *
from functions import seconds_since

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True, use_reloader=True)