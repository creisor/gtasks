import datetime
import time
import logging

from functools import lru_cache
from googleapiclient.discovery import build

# internal packages
from ..src import auth
from .task import Task

@lru_cache
def get_tasklists():
    tasklists = []

    logging.info('authenticating')
    credentials = auth.authenticate()

    service = build('tasks', 'v1', credentials=credentials)
    logging.info('getting tasklists')
    results = service.tasklists().list(maxResults=50).execute()
    items = results.get('items', [])

    for item in items:
        tl = TaskList(item['title'])
        tl.tasks = get_tasks(service, item)

        tasklists.append(tl)

    return tasklists

def get_tasks(service, tasklist):
    tasks = []
    logging.info(f'getting tasks for {tasklist["title"]}')
    items = service.tasks().list(tasklist=tasklist['id'], showCompleted=True, showDeleted=True).execute()
    for item in items['items']:
        tasks.append(Task(item))

    return tasks


class TaskList(object):
    def __init__(self, name):
        self.name = name
        self.tasks = []

    @property
    def date(self):
        return datetime.date(*(time.strptime(self.name, '%m/%d/%Y')[0:3]))
