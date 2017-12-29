import flask
from nomnom import app
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
        poll = Poll.add(form.title.data, form.description.data, form.email.data, form.image_url.data)
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
    delete_form = forms.DeleteForm()
    if delete_form.validate_on_submit():
        poll.key.delete()
        import time
        time.sleep(0.5)
        flask.flash('Poll deleted successfully.', 'success')
        return flask.redirect('/', code=302)  # Redirect back to home page
    form = forms.ResponseForm()
    return flask.render_template('poll.html', title=poll.title, poll=poll, responses=poll.get_responses(), form=form, delete_form=delete_form, delete=True)

# Vote on a response to a poll
@app.route('/poll/<string:poll_id>/vote/<string:vote_type>', methods=['POST'])
def poll_vote(poll_id, vote_type):
    # Check for cookie when voting, and create a cookie if there isn't one
    if 'voteData' in flask.request.cookies:
        cookie = flask.request.cookies.get('voteData')
    else:
        cookie = str(uuid.uuid4())  # Generate cookie
    resp = flask.jsonify({})
    #check the start of vote_type to determin the type of object that the user is voting on
    if vote_type.startswith('resp'):
        # if the user is voting on a response
        r = Response.get_response(poll_id, flask.request.form['resp_id'])
        if vote_type.lower() == 'resp-up':
            r.upvote(cookie)
        elif vote_type.lower() == 'resp-down':
            r.downvote(cookie)
        elif vote_type.lower() == 'resp-flag':
            r.update_flag(cookie)
        resp = flask.jsonify({'score': (r.upv - r.dnv), 'up': r.upv, 'down': r.dnv})
    # if the user is voting on a poll
    elif vote_type.startswith('poll'):
        p = Poll.get_poll(poll_id)
        if vote_type.lower() == 'poll-flag':
            p.update_flag(cookie)
    resp.set_cookie('voteData', cookie)
    return resp

# moderation panel
@app.route('/admin/moderation')
def admin_moderation():
    polls = Poll.get_flagged()
    responses = Response.get_flagged()
    return flask.render_template('moderation.html', polls=polls, responses=responses)

# moderation tools
@app.route('/admin/moderation/<string:poll_id>/action/<string:action_id>', methods=['POST'])
def admin_moderation_action(poll_id, action_id):
    p = Poll.get_poll(poll_id)
    # if the object is a poll
    if action_id.startswith('poll'):
        # approve the poll
        if action_id.endswith('approve'):
            p.mod_approve()
        # remove the poll
        elif action_id.endswith('delete'):
            p.mod_delete()
        return ''
    # if the object is a response
    elif action_id.startswith('response'):
        r = Response.get_response(poll_id, flask.request.form['resp_id'])
        # approve the response
        if action_id.endswith('approve'):
            r.mod_approve()
        # delete the response
        elif action_id.endswith('delete'):
            r.mod_delete()
        return ''
    return ''


## Error Handlers

@app.errorhandler(400)
def error_400(error):
    return flask.render_template('error.html', title='400', heading='Error 400', text="Oh no, that's an error!"), 400

@app.errorhandler(401)
def error_401(error):
    return flask.render_template('error.html', title='401', heading='Error 401', text="Oh no, that's an error!"), 401

@app.errorhandler(403)
def error_403(error):
    return flask.render_template('error.html', title='403', heading='Error 403', text="Oh no, that's an error!"), 403

@app.errorhandler(404)
def error_404(error):
    return flask.render_template('error.html', title='404', heading='Error 404', text="This page does not exist."), 404

@app.errorhandler(405)
def error_405(error):
    return flask.render_template('error.html', title='405', heading='Error 405', text="Oh no, that's an error!"), 405

@app.errorhandler(500)
def error_500(error):
    return flask.render_template('error.html', title='500', heading='Error 500', text="Oh no, that's an error!"), 500
