import flask
from hotspots import app
import logging
import forms
from poll import Poll, Response

# TEMP
polls = [] # Temp poll store during development until we get a database running
def get_poll(id):
    for p in polls:
        if p.id == id:
            return p
    return None
# /TEMP

@app.route('/')
def index():
    return flask.render_template('index.html', title='Index', polls=polls)

# Create a poll
@app.route('/create', methods=['GET', 'POST'])
def create():
    form = forms.CreateForm()
    if form.validate_on_submit():
        poll = Poll(form.title.data, form.description.data)
        polls.append(poll) # Adding to temp store temporarily
        flask.flash('Poll created successfully!', 'success')
        return flask.redirect('/poll/' + poll.id, code=302) # After successfully creating a poll, go to it
    return flask.render_template('create.html', title='Create a Poll', form=form)

# View poll and add responses
@app.route('/poll/<string:poll_id>', methods=['GET', 'POST'])
def poll(poll_id):
    poll = get_poll(poll_id) #TEMP
    if poll is None:
        flask.abort(404)
    form = forms.ResponseForm()
    if form.validate_on_submit():
        poll.responses.append(Response(form.response.data))
    return flask.render_template('poll.html', title=poll.title, poll=poll, form=form)

# Vote on a response to a poll
@app.route('/poll/<string:poll_id>/vote/<string:vote_type>', methods=['POST'])
def poll_vote(poll_id, vote_type):
    poll = get_poll(poll_id) #TEMP
    r = poll.get_response_by_id(flask.request.form['resp_id'])
    if vote_type.lower() == 'up':
        r.upvote()
    elif vote_type.lower() == 'down':
        r.downvote()
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
