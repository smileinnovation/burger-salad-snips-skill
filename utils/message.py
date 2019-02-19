import random

class Message:
    def __init__(self, messages={}, lang='fr'):
        self._lang = lang
        self._messages = messages
        
    @property
    def messages(self):
        return self._messages[self._lang]
    
    def get(self, message_name):
        """
        Send back a random message corresponding to the given message_name.
        """
        if message_name in self.messages:
            m = self.messages[message_name]
            if isinstance(m, list):
                return random.choice(m)
            else:
                return m
