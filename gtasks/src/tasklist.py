import datetime
import time
import logging

from functools import lru_cache
from googleapiclient.discovery import build

# internal packages
from ..src import auth
from .task import Task

@lru_cache
def get_tasklists(name=''):
    # TODO: add a name param and only fetch the named one if there's a name, else fetch them all
    tasklists = []

    logging.info('authenticating')
    credentials = auth.authenticate()

    service = build('tasks', 'v1', credentials=credentials)
    logging.info('getting tasklists')
    results = service.tasklists().list(maxResults=31).execute()
    items = results.get('items', [])

    for item in items:
        logging.debug(f'item: {item}')
        if item['title'] == 'My Tasks':
            continue
        if name:
            if item['title'] != name:
                continue
        tl = TaskList(item['title'])
        tl.tasks = get_tasks(service, item)

        tasklists.append(tl)

    return tasklists

def get_tasks(service, tasklist):
    tasks = []
    logging.info(f'getting tasks for {tasklist["title"]}')
    items = service.tasks().list(
        tasklist=tasklist['id'],
        showCompleted=True,
        # I think sometimes completed tasks show up as deleted
        #showDeleted=True,
        showHidden=True,
    ).execute()
    for item in items['items']:
        logging.debug(f'item: {item}')
        tasks.append(Task(item))

    return tasks


class TaskList(object):
    def __init__(self, name):
        self.name = name
        self.tasks = []

    @property
    def date(self):
        return datetime.date(*(time.strptime(self.name, '%m/%d/%Y')[0:3]))

    def print(self, standup=False):
        if not standup:
            print(f'{self.name}\n---')
        for task in self.tasks:
            task.print(standup)
