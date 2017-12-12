import flask
from nomnom import app
from google.appengine.ext.ndb import Key
from filter import Filter

filter = Filter()


@app.route('/admin/worker/checkresponse', methods=['POST'])
def check_response():
    response = Key(urlsafe=flask.request.form['key']).get()
    if filter.contains_slurs(response.response_str):
        response.mod_flag()
    return '', 200

@app.route('/admin/worker/checkpoll', methods=['POST'])
def check_poll():
    poll = Key(urlsafe=flask.request.form['key']).get()
    if filter.contains_slurs(poll.title) or filter.contains_slurs(poll.description):
        poll.mod_flag()
    return '', 200