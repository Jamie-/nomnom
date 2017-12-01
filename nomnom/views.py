import flask
from nomnom import app
import logging
import forms
from poll import Poll, Response
import uuid

@app.route('/')
def index():
    order = flask.request.args.get("order")
    try:
        return flask.render_template('index.html', polls=Poll.fetch_all(order), order=order)
    except ValueError:
        flask.abort(400)  # Args invalid

# Create a poll
@app.route('/create', methods=['GET', 'POST'])
def create():
    form = forms.CreateForm()
    if form.validate_on_submit():
        poll = Poll.add(form.title.data, form.description.data, form.email.data)
        flask.flash('Poll created successfully', 'success')
        return flask.redirect('/poll/' + poll.get_id(), code=302) # After successfully creating a poll, go to it
    return flask.render_template('create.html', title='Create a Poll', form=form)

# View poll and add responses
@app.route('/poll/<string:poll_id>', methods=['GET', 'POST'])
def poll(poll_id):
    poll = Poll.get_poll(poll_id)
    if poll is None:
        flask.abort(404)
    form = forms.ResponseForm()
    if form.validate_on_submit():
        Response.add(poll, form.response.data)
        flask.flash('Response added', 'success')
    return flask.render_template('poll.html', title=poll.title, poll=poll, responses=poll.get_responses(), form=form)

# Delete a poll
@app.route('/poll/<string:poll_id>/delete/<string:delete_key>', methods=['GET', 'POST'])
def delete_poll(poll_id, delete_key):
    poll = Poll.get_poll(poll_id)
    if poll is None:
        flask.abort(404)
    if poll.delete_key != delete_key:
        flask.abort(403)
    if flask.request.method == 'POST':
        poll.key.delete()
        flask.flash('Poll deleted successfully.', 'success')
        return flask.redirect('/', code=302)  # Redirect back to home page
    form = forms.ResponseForm()
    return flask.render_template('poll.html', title=poll.title, poll=poll, responses=poll.get_responses(), form=form, delete=True)

# Vote on a response to a poll
@app.route('/poll/<string:poll_id>/vote/<string:vote_type>', methods=['POST'])
def poll_vote(poll_id, vote_type):
    # Check for cookie when voting, and create a cookie if there isn't one
    if 'voteData' in flask.request.cookies:
        cookie = flask.request.cookies.get('voteData')
    else:
        cookie = str(uuid.uuid4())  # Generate cookie

    r = Response.get_response(poll_id, flask.request.form['resp_id'])
    if vote_type.lower() == 'up':
        r.upvote(cookie)
    elif vote_type.lower() == 'down':
        r.downvote(cookie)

    resp = flask.jsonify({'score': (r.upv - r.dnv), 'up': r.upv, 'down': r.dnv})
    resp.set_cookie('voteData', cookie)
    return resp


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
