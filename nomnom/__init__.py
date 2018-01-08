from flask import Flask
import flask_socketio
import urllib
import os

app = Flask(__name__)
app.config.from_json('../config.json')
app.jinja_env.globals['APP_NAME'] = app.config['APP_NAME']  # Set global app name in Jinja2 too

socketio = flask_socketio.SocketIO(app)


# URL encode a URL
def url_enc(url):
    return urllib.quote_plus(url)
app.jinja_env.globals.update(url_enc=url_enc)


# Detect development/production environment
def is_production():
    return os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/')
app.jinja_env.globals.update(is_production=is_production)

from nomnom import events
from nomnom import sockets
from nomnom import views
from nomnom import workers
