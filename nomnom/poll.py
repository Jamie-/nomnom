from google.appengine.ext import ndb
from google.appengine.api import taskqueue
import nomnom.tags as tags
from mail import Email
import uuid

# Moderation code, used in both models, so done as a parent class
class NomNomModel(ndb.Model):
    flag = ndb.IntegerProperty()
    flagged_users = ndb.JsonProperty()

    def __init__(self, **kwargs):
        super(NomNomModel, self).__init__(**kwargs)
        self.flag = 0
        self.flagged_users = {}

    # If the wordfilter flags something, automatically hide it
    def mod_flag(self):
        self.flag += 3
        self.put()

    # approve a flagged object, and then make sure it can't be flagged again
    def mod_approve(self):
        self.flag = -1
        self.put()

    # delete a flagged object (no delete key needed)
    def mod_delete(self):
        self.key.delete()

    # Increase flag count
    def update_flag(self, cookie_value):
        # Only allow users to flag once
        if (cookie_value not in self.flagged_users) and (self.flag > -1):
            self.flagged_users[cookie_value] = 1
            self.flag += 1
            self.put()


# Poll object model
class Poll(NomNomModel):
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    email = ndb.StringProperty()
    image_url = ndb.StringProperty()
    delete_key = ndb.StringProperty()
    tag = ndb.StringProperty()
    datetime = ndb.DateTimeProperty(auto_now_add=True)
    visible = ndb.BooleanProperty()

    # can't flag invisible polls
    def update_flag(self, cookie_value):
        if self.visible:
            super(Poll, self).update_flag(cookie_value)

    # get the id of the poll
    def get_id(self):
        return self.key.urlsafe()

    # Get list of response objects
    # flag_count is the number of flags that are required before being excluded from the search (defaults to 3)
    def get_responses(self, n=None, flag_count=3):
        if n is None:
            return sorted(Response.query(Response.flag < flag_count, ancestor=self.key).fetch(), key=lambda response: -response.score)
        else:
            return sorted(Response.query(Response.flag < flag_count, ancestor=self.key).fetch(n), key=lambda response: -response.score)[:n]

    # Checks whether a certain string has already been submitted before
    def check_duplicate(self, response_string):
        responses = self.get_responses()
        for r in responses:
            if r.response_str.lower().strip() == response_string.lower().strip():
                return False
        return True

    # Add poll to datastore
    @classmethod
    def add(cls, title, description, email, image_url, visible):
        content_tag = tags.analyze_entities(title)
        p = Poll(title=title, description=description, email=email, image_url=image_url, delete_key=str(uuid.uuid4()), tag=content_tag, visible=visible)
        p.put()  # Add to datastore
        # don't check hidden polls
        if visible:
            # add a job to a task queue that will check the poll for bad language
            taskqueue.add(queue_name='filter-queue', url='/admin/worker/checkpoll', params={'poll':p.get_id()})
        if email:
            Email.send_mail(email, p.get_id(), p.delete_key)
        return p

    # Fetch all polls from datastore
    # flag_count is the number of flags that are required before being excluded from the search (defaults to 3)
    @classmethod
    def fetch_all(cls, order_by=None, tag_value=None, flag_count=3):
        query = Poll.query(Poll.visible == True, Poll.flag < flag_count)
        # If there is a tag then limit to that tag
        if (tag_value is not None):
            query = Poll.query(Poll.visible == True, Poll.flag < flag_count, Poll.tag == tag_value)
        if (order_by is None):  # First as most common case
            return sorted(query.fetch())
        elif (order_by == "newest"):
            return query.order(Poll.flag).order(-Poll.datetime).fetch()
        elif (order_by == "hottest"):
            return sorted(query.fetch(), key=lambda poll: -sum(r.upv + r.dnv for r in Response.query(ancestor=poll.key).fetch()))
        elif (order_by == "easiest"):
            return sorted(query.fetch(), key=lambda poll: Response.query(ancestor=poll.key).count())
        raise ValueError()  # order_by not in specified list

    # Get poll from datastore by ID
    @classmethod
    def get_poll(cls, id):
        key = ndb.Key(urlsafe=id)
        return key.get()

    # Get the flagged polls from the datastore
    @classmethod
    def get_flagged(cls, flag_count=3):
        return Poll.query(Poll.flag >= flag_count).fetch()


# Response object model
class Response(NomNomModel):
    response_str = ndb.StringProperty()
    upv = ndb.IntegerProperty()
    dnv = ndb.IntegerProperty()
    score = ndb.ComputedProperty(lambda self: self.upv - self.dnv)
    voted_users = ndb.JsonProperty()

    # Initialise a new response object with 0 upv and dnv maintaining kwargs to parent
    def __init__(self, **kwargs):
        super(Response, self).__init__(**kwargs) # Call parent constructor
        self.upv = 0
        self.dnv = 0
        self.voted_users = {}

    # Get the id of the response
    def get_id(self):
        return self.key.id()

    # Get the id of the parent poll
    def get_poll_id(self):
        return self.key.parent().urlsafe()

    # Add up-vote to response
    def upvote(self, cookie_value):
        vote_value = 0
        if cookie_value in self.voted_users:
            vote_value = self.voted_users[cookie_value]

        if vote_value == 1:  # User has previously upvoted (so toggle vote)
            self.upv -= 1
            self.voted_users[cookie_value] = 0
        elif vote_value == 0:  # User has no previous vote
            self.upv += 1
            self.voted_users[cookie_value] = 1
        elif vote_value == -1:  # User has previously downvoted (so change vote)
            self.upv += 1
            self.dnv -= 1
            self.voted_users[cookie_value] = 1

        self.put()

    # Add down-vote to response
    def downvote(self, cookieValue):
        vote_value = 0
        if cookieValue in self.voted_users:
            vote_value = self.voted_users[cookieValue]

        if vote_value == -1:  # User has previously downvoted (so toggle vote)
            self.dnv -= 1
            self.voted_users[cookieValue] = 0
        elif vote_value == 0:  # User has no previous vote
            self.dnv += 1
            self.voted_users[cookieValue] = -1
        elif vote_value == 1:  # User has previously upvoted (so change vote)
            self.upv -= 1
            self.dnv += 1
            self.voted_users[cookieValue] = -1

        self.put()

    # Add response to datastore
    @classmethod
    def add(cls, poll, response_str):
        r = Response(parent=poll.key, response_str=response_str)
        r.put()
        # if the poll is public schedule a thread to check the response for bad language
        if r.poll_visible():
            taskqueue.add(queue_name='filter-queue', url='/admin/worker/checkresponse', params={'poll':poll.get_id(), 'response':r.get_id()})
        return r

    # Check if the parent poll is visible.
    def poll_visible(self):
        return self.key.parent().get().visible

    # don't flag responses to hidden polls
    def update_flag(self, cookie_value):
        if self.poll_visible():
            super(Response, self).update_flag(cookie_value)

    # Get response from datastore
    @classmethod
    def get_response(cls, poll_id, response_id):
        poll = ndb.Key(urlsafe=poll_id).get()
        resp_id = int(response_id)
        return Response.get_by_id(resp_id, parent=poll.key)

    # Get flagged responses
    @classmethod
    def get_flagged(cls, flag_count=3):
        return Response.query(Response.flag >= flag_count).fetch()
