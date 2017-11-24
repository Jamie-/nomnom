from google.appengine.ext import ndb

# Poll object model
class Poll(ndb.Model):
    title = ndb.StringProperty()
    description = ndb.TextProperty()

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
    def add(cls, title, description):
        p = Poll(title=title, description=description)
        p.put() # Add to datastore
        return p

    # Fetch all polls from datastore
    @classmethod
    def fetch_all(cls):
        query = Poll.query()
        return query.fetch()

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
    score = ndb.ComputedProperty(lambda self: self.upv - self.dnv)
    voted_users = ndb.JsonProperty()

    # Initialise a new response object with 0 upv and dnv maintaining kwargs to parent
    def __init__(self, **kwargs):
        super(Response, self).__init__(**kwargs) # Call parent constructor
        self.upv = 0
        self.dnv = 0
        self.voted_users = {}


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
