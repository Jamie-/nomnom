from google.appengine.ext import ndb
import math

# Poll object model
class Poll(ndb.Model):
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    datetime = ndb.DateTimeProperty(auto_now_add=True)
    location = ndb.GeoPtProperty()

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
    def add(cls, title, description, lon, lat):
        p = Poll(title=title, description=description, location=ndb.GeoPt(lat,lon))
        p.put() # Add to datastore
        return p

    # Fetch all polls from datastore
    @classmethod
    def fetch_all(cls, order_by=None, location=None):
        query = ""
        if (order_by == "newest"):
            query = Poll.query().order(-Poll.datetime)
        elif (order_by == "oldest"):
            query = Poll.query().order(Poll.datetime)
        else:
           query = Poll.query()
        polls = query.fetch()
        if (order_by == "closest"):
            return polls.sort(key=lambda p: math.fabs(
                Poll.getDistanceFromLatLonInKm(location[0], location[1], p.location.lat, p.location.lon)))
        return query.fetch()

    def getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2):
        R = 6371
        dLat = (lat2 - lat1)* (math.PI / 180)
        dLon = (lon2 - lon1)* (math.PI / 180)
        a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos((lat1)* (math.PI / 180)) * math.cos((lat2)* (math.PI / 180)) * math.sin(dLon / 2) * math.sin(dLon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c
        return d

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
