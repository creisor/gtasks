import re

class Task(object):
    def __init__(self, item):
        self.item = item

    @property
    def name(self):
        return self.item['title']

    @property
    def is_personal(self):
        if self.item['title'].startswith('personal'):
            return True
        return False

    @property
    def is_complete(self):
        try:
            if self.item['deleted']:
                return True
            else:
                return False
        except KeyError:
            if self.item['status'] == 'completed':
                return True
            else:
                return False

        return False

    def print(self, standup=False, personal=False):
        if self.is_personal and not personal:
            return

        print(self.name)
