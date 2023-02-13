from functools import lru_cache
from ..src import auth

@lru_cache
def get_tasklists():
    tasklists = []

    credentials = auth.authenticate()

    service = build('tasks', 'v1', credentials=credentials)
    results = service.tasklists().list(maxResults=10).execute()

    return tasklists

class Tasklist(object):
    def __init__(self, name):
        self.name = name

    @property
    def tasks(self):
        pass
