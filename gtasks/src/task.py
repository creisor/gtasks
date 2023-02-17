import re

class Task(object):
    def __init__(self, item):
        self.item = item

    @property
    def name(self):
        return self.item['title']

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

    def print(self, standup=False):
        msg = ''
        if self.is_complete and standup:
            msg += '[COMPLETE] '
        if standup:
            msg += '* '
            msg += re.sub(r'(?P<ticket>[A-Z]{3,}-\d{3,})', '`\g<ticket>`', self.name)
        else:
            msg += self.name

        print(msg)
