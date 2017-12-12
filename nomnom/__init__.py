from flask import Flask
import urllib

app = Flask(__name__)
app.config.from_json('../config.json')
app.jinja_env.globals['APP_NAME'] = app.config['APP_NAME'] # Set global app name in Jinja2 too

# URL encode a URL
def url_enc(url):
    return urllib.quote_plus(url)
app.jinja_env.globals.update(url_enc=url_enc)

from nomnom import views
from nomnom import workers

