# Generic callable event
class Event():


    def __init__(self):
        self._observers = set()


    # Add a listener
    def add_listener(self, listener):
        self._observers.add(listener)


    # Remove a listener
    def remove_listener(self, listener):
        self._observers.remove(listener)

    # Fire the event
    def fire(self, *args):
        for observer in self._observers:
            observer(*args)


    __call__ = fire  # Fire event if called
