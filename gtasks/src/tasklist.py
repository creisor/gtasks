from functools import lru_cache
from googleapiclient.discovery import build

# internal packages
from ..src import auth
from .task import Task

@lru_cache
def get_tasklists():
    tasklists = []

    credentials = auth.authenticate()

    service = build('tasks', 'v1', credentials=credentials)
    results = service.tasklists().list(maxResults=50).execute()
    items = results.get('items', [])

    for item in items:
        tl = TaskList(item['title'])
        tl.tasks = get_tasks(service, item)

        tasklists.append(tl)

    return tasklists

def get_tasks(service, tasklist):
    tasks = []
    items = service.tasks().list(tasklist=tasklist['id'], showCompleted=True, showDeleted=True).execute()
    for item in items['items']:
        tasks.append(Task(item))

    return tasks


class TaskList(object):
    def __init__(self, name):
        self.name = name
        self.tasks = []

    #@property
    #def tasks(self):
    #    pass
