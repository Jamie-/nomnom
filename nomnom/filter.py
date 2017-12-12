import requests

################
# Filter Class #
################
class Filter:
    # create the class
    def __init__(self):
        self._url = "http://www.purgomalum.com/service/containsprofanity?text="

    def contains_slurs(self, string):
        r = requests.get(self._url+string)
        if r.text == 'true':
            return True
        else:
            return False


