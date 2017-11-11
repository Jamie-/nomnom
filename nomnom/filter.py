from __future__ import print_function
import json
import re


class Filter:
    def __init__(self, fs_path):
        with open(fs_path) as fs_file:
            filter_settings = json.loads(fs_file)
        word_list = filter_settings['word_list']
        regex_patterns = filter_settings['regex']
        keys = sorted(regex_patterns.keys())
        for i in range(len(word_list)):
            word = word_list[i]
            for key in keys:
                word.replace(key, regex_patterns[key])
            word_list[i] = word
        self._word_list = word_list

    def is_safe(self, string):
        for word in self._word_list:
            match = re.search(word, string)
            if match:
                return False
        return True
