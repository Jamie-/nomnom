import uuid

# Poll object model
class Poll():

    def __init__(self, title, description):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.responses = []

    # Get a response object by ID
    def get_response_by_id(self, response_id):
        for r in self.responses:
            if r.id == response_id:
                return r
        return None

    # Get top three responses
    #TODO order by score in this rankning - needs DB
    def get_top_three(self):
        if len(self.responses) < 4:
            return self.responses
        else:
            return self.responses[:3]


# Response object model
class Response():

    def __init__(self, response_str):
        self.id = str(uuid.uuid4())
        self.response_str = response_str
        self.upv = 0
        self.dnv = 0

    # Add up-vote to response
    def upvote(self):
        self.upv += 1

    # Add down-vote to response
    def downvote(self):
        self.dnv += 1
