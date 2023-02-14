class Task(object):
    def __init__(self, item):
        self.item = item

    @property
    def name(self):
        return self.item['title']

    def is_complete(self):
        try:
            if self.item['deleted']:
                return True
        except KeyError:
            return False

        return False
