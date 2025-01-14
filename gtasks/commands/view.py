import click
import logging
import sys
from datetime import date, timedelta
from googleapiclient.discovery import build

# internal packages
from ..src import auth
from ..src import tasklist

@click.command()
@click.option('-y', '--yesterday', is_flag=True, help='See yesterday\'s tasks')
@click.option('-d', '--date', "list_date", help='See tasks for <date>. Use MM/DD/YYYY format.')
@click.option('-a', '--all-tasks', is_flag=True, help='See tasks from all tasklists')
@click.option('-s', '--standup', is_flag=True, help='Print tasks in standup format')
def view(yesterday, list_date, all_tasks, standup):
    """Allows you to view tasks in your list(s)"""

    today = date.today()

    if yesterday:
        tasklist_name = (today - timedelta(hours=24)).strftime('%m/%d/%Y')
    elif list_date:
        tasklist_name = list_date
    else:
        tasklist_name = today.strftime('%m/%d/%Y')

    logging.info('authenticating')
    credentials = auth.authenticate()
    service = build('tasks', 'v1', credentials=credentials)

    if all_tasks:
        tasklists = tasklist.get_tasklists(service)

        for tl in tasklists:
            tl.print(standup)

    else:
        try:
            tl = tasklist.get_tasklists(service, tasklist_name)[0]
        except IndexError:
            print(f'I tried, but found no task entitled {tasklist_name}')
            sys.exit(0)
        tl.print(standup)
