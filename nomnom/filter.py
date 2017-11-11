from __future__ import print_function
import json
import re
import unittest


class Filter:
    # create the class
    def __init__(self, fs_path):
        # open the json file and read the contents
        with open(fs_path, 'r') as fs_file:
            filter_settings = json.load(fs_file)
        # take out the word list and the regex
        word_list = filter_settings['word_list']
        regex_patterns = filter_settings['regex']
        # sort the keys to the regex, they need to be in alphabetical order
        keys = sorted(regex_patterns.keys())
        # go through the word list
        for i in range(len(word_list)):
            word = word_list[i]
            for key in keys:
                # replace each occurence of a letter character, with it's regex.
                word = word.replace(key, regex_patterns[key])
            # add in surrounding regex
            # (?<![a-z]) and (?![a-z]) means that the word won't trigger if surrounded by letters
            # (ed|ing|es|s)? : common english conjugations
            word = '(?<![a-z])' + word + '(ed|ing|es|s)?(?![a-z])'
            # add the word back to the list
            word_list[i] = word
        # save the list
        self._word_list = word_list

    def is_safe(self, string):
        # put the string in lowercase
        string = string.lower()
        for word in self._word_list:
            # if the word regex is found in the string, the string is not safe
            search = re.search(word, string)
            if search:
                return False
        # if the regex is never triggered the string is safe.
        return True


##########################################################
# Class used for unit testing, no need to use in project.#
##########################################################
class TestFilter(unittest.TestCase):
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
