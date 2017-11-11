import json


class Filter:
    def __init__(self, wl_path):
        with open(wl_path) as wl_file:
            self._wordlist = json.loads(wl_file)

    def is_obscene(self, string):
        for word in self._wordlist:
            if ' {} '.format(word) in string:
                return True
        return False
