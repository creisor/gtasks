import click
import datetime
import logging

# internal packages
from ..src import tasklist

@click.command()
@click.option('-y', '--yesterday', is_flag=True, help='See yesterday\'s tasks')
@click.option('-a', '--all-tasks', is_flag=True, help='See tasks from all tasklists')
def view(yesterday, all_tasks):
    """Allows you to view tasks in your list(s)"""

    tasklists = tasklist.get_tasklists()

    today = datetime.date.today()

    if all_tasks:
        print('view all')

    elif yesterday:
        tasklists.reverse()
        y = [t for t in tasklists if (today - t.date).days == 1]
        l = y[0]
        print(l.name)
        print('----')
        for task in l.tasks:
            task.print()

    else:
        print('view today')
