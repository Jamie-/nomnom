from google.appengine.ext import ndb
import nomnom.tags as tags
from mail import Email
import uuid

# Poll object model
class Poll(ndb.Model):
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    datetime = ndb.DateTimeProperty(auto_now_add=True)
    email = ndb.StringProperty()
    image_url = ndb.StringProperty()
    delete_key = ndb.StringProperty()
    tag = ndb.StringProperty()

    def get_id(self):
        return self.key.urlsafe()

    # Get list of response objects
    def get_responses(self, n=None):
        if n is None:
            return sorted(Response.query(ancestor=self.key).fetch(), key=lambda response: -response.score)
        else:
            return sorted(Response.query(ancestor=self.key).fetch(n), key=lambda response: -response.score)[:n]

    # Add poll to datastore
    @classmethod
    def add(cls, title, description, email, image_url):
        content_tag = tags.entities_text(title)
        p = Poll(title=title, description=description, email=email, image_url=image_url, delete_key=str(uuid.uuid4()), tag=content_tag)
        p.put()  # Add to datastore
        if email:
            Email.send_mail(email, p.get_id(), p.delete_key)
        return p

    # Fetch all polls from datastore
    @classmethod
    def fetch_all(cls, order_by=None, tag_value=None):
        # If there is a tag then write query
        query = Poll.query()
        if(tag_value is not None):
            query = Poll.query(Poll.tag == tag_value)
        if (order_by is None):  # First as most common case
            return query.fetch()
        elif (order_by == "newest"):
            return query.order(-Poll.datetime).fetch()
        elif (order_by == "oldest"):
            return query.order(Poll.datetime).fetch()
        elif (order_by == "hottest"):
            return sorted(query.fetch(), key=lambda poll: -sum(r.upv + r.dnv for r in Response.query(ancestor=poll.key).fetch()))
        elif (order_by == "coldest"):
            return sorted(query.fetch(), key=lambda poll: sum(r.upv + r.dnv for r in Response.query(ancestor=poll.key).fetch()))
        elif (order_by == "easiest"):
            return sorted(query.fetch(), key=lambda poll: Response.query(ancestor=poll.key).count())
        elif (order_by == "hardest"):
            return sorted(query.fetch(), key=lambda poll: -Response.query(ancestor=poll.key).count())
        raise ValueError()  # order_by not in specified list

    # Get poll from datastore by ID
    @classmethod
    def get_poll(cls, id):
        key = ndb.Key(urlsafe=id)
        return key.get()


# Response object model
class Response(ndb.Model):
    response_str = ndb.StringProperty()
    upv = ndb.IntegerProperty()
    dnv = ndb.IntegerProperty()
    flag = ndb.IntegerProperty()
    score = ndb.ComputedProperty(lambda self: self.upv - self.dnv)
    voted_users = ndb.JsonProperty()
    flagged_users = ndb.JsonProperty()

    # Initialise a new response object with 0 upv and dnv maintaining kwargs to parent
    def __init__(self, **kwargs):
        super(Response, self).__init__(**kwargs) # Call parent constructor
        self.upv = 0
        self.dnv = 0
        self.flag = 0
        self.voted_users = {}
        self.flagged_users = {}


    def get_id(self):
        return self.key.id()

    # Add up-vote to response
    def upvote(self, cookieValue):
        vote_value = 0
        if cookieValue in self.voted_users:
            vote_value = self.voted_users[cookieValue]

        if vote_value == 1:  # User has previously upvoted (so toggle vote)
            self.upv -= 1
            self.voted_users[cookieValue] = 0
        elif vote_value == 0:  # User has no previous vote
            self.upv += 1
            self.voted_users[cookieValue] = 1
        elif vote_value == -1:  # User has previously downvoted (so change vote)
            self.upv += 1
            self.dnv -= 1
            self.voted_users[cookieValue] = 1

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

    # Increase flag count
    def update_flag(self, cookie_value):
        # Only allow users to flag once
        if cookie_value not in self.flagged_users:
            self.flagged_users[cookie_value] = 0
            self.flag += 1
            self.put()

    # Add response to datastore
    @classmethod
    def add(cls, poll, response_str):
        r = Response(parent=poll.key, response_str=response_str)
        r.put()
        return r

    # Get response from datastore
    @classmethod
    def get_response(cls, poll_id, response_id):
        poll = ndb.Key(urlsafe=poll_id).get()
        resp_id = int(response_id)
        return Response.get_by_id(resp_id, parent=poll.key)
