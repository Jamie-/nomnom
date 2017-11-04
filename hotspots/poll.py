import uuid

# Poll object model
from google.appengine.ext import ndb


class Poll(ndb.Model):

    title = ndb.StringProperty()
    description = ndb.TextProperty()

    responses = []

    def set_responses(self, n):
        self.responses = Response.query(ancestor=self.key).fetch(n)
        return


# Response object model
class Response(ndb.Model):

    response_str = ndb.StringProperty()
    upv = ndb.IntegerProperty()
    dnv = ndb.IntegerProperty()
