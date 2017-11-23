from google.appengine.ext import ndb

# Poll object model
class Poll(ndb.Model):
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    datetime = ndb.DateTimeProperty(auto_now_add=True)

    def get_id(self):
        return self.key.urlsafe()

    # Get list of response objects
    def get_responses(self, n=None):
        if n is None:
            return Response.query(ancestor=self.key).fetch()
        else:
            return Response.query(ancestor=self.key).fetch(n)

    # Add poll to datastore
    @classmethod
    def add(cls, title, description):
        p = Poll(title=title, description=description)
        p.put() # Add to datastore
        return p

    # Fetch all polls from datastore
    @classmethod
    def fetch_all(cls, order_by=None):
        if (order_by is None):  # First as most common case
            return Poll.query().fetch()
        if (order_by == "newest"):
            return Poll.query().order(-Poll.datetime).fetch()
        elif (order_by == "oldest"):
            return Poll.query().order(Poll.datetime).fetch()
        elif (order_by == "hottest"):
            return sorted(Poll.query().fetch(), key=lambda poll: -sum(r.upv + r.dnv for r in Response.query(ancestor=poll.key).fetch()))
        elif (order_by == "coldest"):
            return sorted(Poll.query().fetch(), key=lambda poll: sum(r.upv + r.dnv for r in Response.query(ancestor=poll.key).fetch()))
        elif (order_by == "easiest"):
            return sorted(Poll.query().fetch(), key=lambda poll: Response.query(ancestor=poll.key).count())
        elif (order_by == "hardest"):
            return sorted(Poll.query().fetch(), key=lambda poll: -Response.query(ancestor=poll.key).count())
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

    # Initialise a new response object with 0 upv and dnv maintaining kwargs to parent
    def __init__(self, **kwargs):
        super(Response, self).__init__(**kwargs) # Call parent constructor
        self.upv = 0
        self.dnv = 0

    def get_id(self):
        return self.key.id()

    # Add up-vote to response
    def upvote(self):
        self.upv += 1
        self.put() # Update in datastore

    # Add down-vote to response
    def downvote(self):
        self.dnv += 1
        self.put() # Update in datastore

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
