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
        except KeyError:
            return False

        return False

    def print(self):
        msg = ''
        if self.is_complete:
            msg += '[COMPLETE] '
        msg += self.name

        import pdb; pdb.set_trace()

        print(msg)
