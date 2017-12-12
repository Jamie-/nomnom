import requests

################
# Filter Class #
################
class Filter:
    # create the class
    def __init__(self):
        self._url = "http://www.purgomalum.com/service/containsprofanity?text="

    def is_safe(self, string):
        print "Checking: \'"+string + "'"
        r = requests.get(self._url+string)
        print r.text
        if r.text == 'true':
            return False
        else:
            return True


