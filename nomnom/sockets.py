import flask_socketio
import json
from nomnom import socketio, is_production
from nomnom import events


# Display successful connection message in dev environment
@socketio.on('connect')
def connect():
    if not is_production():
        socketio.send('Welcome to the server, you are connected!')


# Push poll data to clients for live update
def push_poll(poll):
    if poll.visible:  # Only push if poll is visible
        data = {}
        data['poll'] = {}
        data['poll']['id'] = poll.get_id()
        data['poll']['title'] = poll.title
        data['poll']['description'] = poll.description
        if poll.image_url is not None and poll.image_url != "":
            data['poll']['image_url'] = poll.image_url
        data['poll']['tag'] = poll.tag
        socketio.send(json.dumps(data), json=True)


# Push response data to clients for live update
def push_response(response):
    if response.poll_visible():  # Only push if containing poll is visible
        data = {}
        data['response'] = {}
        data['response']['id'] = response.get_id()
        data['response']['poll'] = response.get_poll_id()
        data['response']['string'] = response.response_str
        data['response']['score'] = response.score
        data['response']['upv'] = response.upv
        data['response']['dnv'] = response.dnv
        socketio.send(json.dumps(data), json=True)
    else:  # Only push to users viewing the poll
        pass  #TODO this


# Push votes to clients for live update
def push_vote(response):
    if response.poll_visible():  # Only push if containing poll is visible
        data = {}
        data['vote'] = {}
        data['vote']['poll_id'] = response.get_poll_id()
        data['vote']['response_id'] = response.get_id()
        data['vote']['score'] = response.score
        data['vote']['upv'] = response.upv
        data['vote']['dnv'] = response.dnv
        socketio.send(json.dumps(data), json=True)
    else:  # Only push to users viewing the poll
        pass  #TODO this


# Add event handlers
events.poll_created_event.add_listener(push_poll)
events.response_event.add_listener(push_response)
events.vote_event.add_listener(push_vote)
