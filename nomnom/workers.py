import flask
from nomnom import app
import json
from poll import Poll, Response
from google.appengine.ext.ndb import Key
from filter import Filter

filter = Filter()


@app.route('/admin/worker/checkresponse', methods=['POST'])
def check_response():
    response = Key(urlsafe=flask.request.form['key']).get()
    print response.response_str
    if not filter.is_safe(response.response_str):
        response.mod_flag()
    return '', 200

