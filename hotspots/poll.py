import uuid

# Poll object model
from google.appengine.ext import ndb


class Poll(ndb.Model):

    title = ndb.StringProperty()
    description = ndb.TextProperty()


# Response object model
class Response(ndb.Model):

    response_str = ndb.StringProperty()
    upv = ndb.IntegerProperty()
    dnv = ndb.IntegerProperty()
