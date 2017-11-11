from __future__ import print_function
import json
import re
import unittest


class Filter:
    def __init__(self, fs_path):
        with open(fs_path, 'r') as fs_file:
            filter_settings = json.load(fs_file)
        word_list = filter_settings['word_list']
        regex_patterns = filter_settings['regex']
        keys = sorted(regex_patterns.keys())
        for i in range(len(word_list)):
            word = word_list[i]
            for key in keys:
                word = word.replace(key, regex_patterns[key])
            word = '(?<![a-z])' + word + '(ed|ing|es|s)?(?![a-z])'
            word_list[i] = word
        self._word_list = word_list

    def is_safe(self, string):
        string = string.lower()
        for word in self._word_list:
            search = re.search(word, string)
            if search:
                return False
        return True


class TestFilter(unittest.TestCase):
    def setUp(self):
        self.filter = Filter('bad_words.json')

    # Check basic regex matches
    def test_match(self):

        # lower case
        self.assertFalse(self.filter.is_safe('bitch'))

        # mixed case
        self.assertFalse(self.filter.is_safe('niGGer'))

        # l33t speak
        self.assertFalse(self.filter.is_safe('f4gg0t'))

    # The Scunthorpe problem
    def test_scunthorpe(self):
        self.assertTrue(self.filter.is_safe('Scunthorpe'))

    # test the word in a sentence.
    def test_in_context(self):
        self.assertFalse(self.filter.is_safe('Bitches, bitches, bitches. I love fucking Bitches.'))
        
    def test_passes(self):
        self.assertTrue(self.filter.is_safe('Hello there, I have a bird.'))
        
        self.assertTrue(self.filter.is_safe('Magpie'))


if __name__ == '__main__':
    unittest.main()
