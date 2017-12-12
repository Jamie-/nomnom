import unittest
from wtforms import ValidationError
import urllib

################
# Filter Class #
################
class Filter:
    # create the class
    def __init__(self):
        self._url = "http://www.purgomalum.com/service/containsprofanity?text="

    def is_safe(self, string):
        with urllib.request.urlopen(self._url+string) as r:
            text =  r.read()
        if text == 'true':
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


##########################################################
# Class used for unit testing, no need to use in project.#
##########################################################
class _TestFilter(unittest.TestCase):
    def setUp(self):
        self.filter = Filter('bad_words.json')

    # should catch the words used individually
    def test_match(self):

        # lower case
        self.assertFalse(self.filter.is_safe('bitch'))

        # mixed case
        self.assertFalse(self.filter.is_safe('niGGer'))

        # l33t speak
        self.assertFalse(self.filter.is_safe('f4gg0t'))

    # The Scunthorpe problem, shouldn't trigger the catch
    def test_scunthorpe(self):
        self.assertTrue(self.filter.is_safe('Scunthorpe'))

    # test the word in a sentence, should see these
    def test_in_context(self):
        self.assertFalse(self.filter.is_safe('Bitches, bitches, bitches. I love fucking Bitches.'))

    # these should both passes, being safe words.
    def test_passes(self):
        self.assertTrue(self.filter.is_safe('Hello there, I have a bird.'))
        
        self.assertTrue(self.filter.is_safe('Magpie'))


if __name__ == '__main__':
    unittest.main()
