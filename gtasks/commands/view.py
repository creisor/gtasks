import click
import logging
import sys
from datetime import date, timedelta

# internal packages
from ..src import tasklist

@click.command()
@click.option('-y', '--yesterday', is_flag=True, help='See yesterday\'s tasks')
@click.option('-a', '--all-tasks', is_flag=True, help='See tasks from all tasklists')
@click.option('-s', '--standup', is_flag=True, help='Print tasks in standup format')
def view(yesterday, all_tasks, standup):
    """Allows you to view tasks in your list(s)"""


    today = date.today()

    if all_tasks:
        tasklists = tasklist.get_tasklists()

        for tl in tasklists:
            tl.print(standup)

    elif yesterday:
        tasklist_name = (today - timedelta(hours=24)).strftime('%m/%d/%Y')
        try:
            tl = tasklist.get_tasklists(tasklist_name)[0]
        except IndexError:
            print(f'I tried to get yesterday\'s tasklist, but there is no task entitled {tasklist_name}')
            sys.exit(0)
        tl.print(standup)

    else:
        tasklist_name = today.strftime('%m/%d/%Y')

        try:
            tl = tasklist.get_tasklists(tasklist_name)[0]
        except IndexError:
            print(f'I tried to get today\'s tasklist, but there is no task entitled {tasklist_name}')
            sys.exit(0)
        tl.print(standup)
