import unittest
from wtforms import ValidationError
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


####################
# Language Checker #
####################
class Language(object):
    def __init__(self):
        self._filter = Filter()
        self._message = 'There is inappropriate language in this field.'

    def __call__(self, form, field):
        string = field.data
        if not self._filter.is_safe(string):
            raise ValidationError(self._message)


if __name__ == '__main__':
    unittest.main()
