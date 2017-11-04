import flask
from hotspots import app
import logging
import forms
from poll import Poll, Response
from google.appengine.ext import ndb

@app.route('/')
def index():
    return flask.render_template('index.html', polls=Poll.query().fetch())

# Create a poll
@app.route('/create', methods=['GET', 'POST'])
def create():
    form = forms.CreateForm()
    if form.validate_on_submit():
        poll = Poll(title = form.title.data, description = form.description.data)
        poll.put()
        flask.flash('Poll created successfully!', 'success')
        return flask.redirect('/poll/' + poll.key.urlsafe(), code=302) # After successfully creating a poll, go to it
    return flask.render_template('create.html', title='Create a Poll', form=form)

# View poll and add responses
@app.route('/poll/<string:poll_id>', methods=['GET', 'POST'])
def poll(poll_id):
    poll_key = ndb.Key(urlsafe=poll_id)
    poll = poll_key.get()
    if poll is None:
        flask.abort(404)
    form = forms.ResponseForm()
    if form.validate_on_submit():
        r = Response(parent = poll.key, response_str = form.response.data)
        r.put()
    rs = Response.query(ancestor=poll.key).fetch()
    return flask.render_template('poll.html', title=poll.title, poll=poll, form=form, responses = rs)

# Vote on a response to a poll
@app.route('/poll/<string:poll_id>/vote/<string:vote_type>', methods=['POST'])
def poll_vote(poll_id, vote_type):
    poll = ndb.Key(urlsafe=poll_id).get()
    r = Response.query(ancestor=poll.key, id = flask.request.form['resp_id']).fetch()
    if vote_type.lower() == 'up':
        r.upv += 1
    elif vote_type.lower() == 'down':
        r.dnv += -1
    r.put()
    return flask.jsonify({'score': (r.upv - r.dnv), 'up': r.upv, 'down': r.dnv})


## Error Handlers

@app.errorhandler(400)
def error_400(error):
    return flask.render_template('error.html', title='400', heading='Error 400', text="Oh no, that's an error!")

@app.errorhandler(401)
def error_401(error):
    return flask.render_template('error.html', title='401', heading='Error 401', text="Oh no, that's an error!")

@app.errorhandler(403)
def error_403(error):
    return flask.render_template('error.html', title='403', heading='Error 403', text="Oh no, that's an error!")

@app.errorhandler(404)
def error_404(error):
    return flask.render_template('error.html', title='404', heading='Error 404', text="Oh no, that's an error!")

@app.errorhandler(405)
def error_405(error):
    return flask.render_template('error.html', title='405', heading='Error 405', text="Oh no, that's an error!")

@app.errorhandler(500)
def error_500(error):
    return flask.render_template('error.html', title='500', heading='Error 500', text="Oh no, that's an error!")
