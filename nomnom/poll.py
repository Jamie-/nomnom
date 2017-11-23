from google.appengine.ext import ndb

# Poll object model
class Poll(ndb.Model):
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    hotness = ndb.IntegerProperty()
    datetime = ndb.DateTimeProperty(auto_now_add=True)
    responses = ndb.IntegerProperty()

    def get_id(self):
        return self.key.urlsafe()

    # Get list of response objects
    def get_responses(self, n=None):
        if n is None:
            return Response.query(ancestor=self.key).fetch()
        else:
            return Response.query(ancestor=self.key).fetch(n)

    # Calculate how hot a poll is
    def set_hotness(self):
        responses = Response.query(ancestor=self.key).fetch()
        hotness = 0
        for response in responses:
            hotness = hotness + response.upv
            hotness = hotness - response.dnv
        self.hotness = hotness
        self.put()

    # Calculate no. of responses on a poll
    def set_responses(self):
        responses = Response.query(ancestor=self.key).fetch()
        self.responses = len(responses)
        self.put()

    # Add poll to datastore
    @classmethod
    def add(cls, title, description):
        p = Poll(title=title, description=description, hotness=0)
        p.put() # Add to datastore
        return p

    # Fetch all polls from datastore
    @classmethod
    def fetch_all(cls, order_by=None):
        query = ""
        if (order_by == "newest"):
            query = Poll.query().order(-Poll.datetime)
        elif (order_by == "oldest"):
            query = Poll.query().order(Poll.datetime)
        elif (order_by == "hotest" or order_by == "coldest"):
            # Set the hotness on each poll
            query = Poll.query()
            polls = query.fetch()
            for poll in polls:
                poll.set_hotness()
            if(order_by == "hotest"):
                query = Poll.query().order(-Poll.hotness)
            else:
                query = Poll.query().order(Poll.hotness)
        elif (order_by == "easiest" or order_by == "hardest"):
            # Set the hotness on each poll
            query = Poll.query()
            polls = query.fetch()
            for poll in polls:
                poll.set_responses()
            if(order_by == "easiest"):
                query = Poll.query().order(-Poll.responses)
            else:
                query = Poll.query().order(Poll.responses)
        else:
            query = Poll.query()
        polls = query.fetch()
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
