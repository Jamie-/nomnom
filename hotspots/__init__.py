from flask import Flask

app = Flask(__name__)
app.config.from_json('../config.json')
app.jinja_env.globals['APP_NAME'] = app.config['APP_NAME'] # Set global app name in Jinja2 too

from hotspots import views
