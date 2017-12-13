import flask
from nomnom import app
from google.appengine.ext.ndb import Key
from poll import Response, Poll
from filter import Filter

filter = Filter()


@app.route('/admin/worker/checkresponse', methods=['POST'])
def check_response():
    response = Response.get_response(flask.request.form['poll'], flask.request.form['response'])
    if filter.contains_slurs(response.response_str):
        response.mod_flag()
    return '', 200

@app.route('/admin/worker/checkpoll', methods=['POST'])
def check_poll():
    poll = Poll.get_poll(flask.request.form['poll'])
    if filter.contains_slurs(poll.title) or filter.contains_slurs(poll.description):
        poll.mod_flag()
    return '', 200