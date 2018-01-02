import flask
from nomnom import app
from poll import Response, Poll
from filter import Filter

filter = Filter()

# Views that are only ever accessed by GAE worker threads, such as task queues or cronjobs go here

# Check for bad language in a response
@app.route('/admin/worker/checkresponse', methods=['POST'])
def check_response():
    response = Response.get_response(flask.request.form['poll'], flask.request.form['response'])
    if filter.contains_slurs(response.response_str):
        response.mod_flag()
    return '', 200

# Check for bad language in a poll
@app.route('/admin/worker/checkpoll', methods=['POST'])
def check_poll():
    poll = Poll.get_poll(flask.request.form['poll'])
    if filter.contains_slurs(poll.title) or filter.contains_slurs(poll.description):
        poll.mod_flag()
    return '', 200
