import urllib2

################
# Filter Class #
################
class Filter:
    # create the class
    def __init__(self):
        self._url = "http://www.purgomalum.com/service/containsprofanity?text="

    def contains_slurs(self, string):
        r = urllib2.urlopen(self._url+string)
        text = r.read()
        if text == 'true':
            return True
        else:
            return False


