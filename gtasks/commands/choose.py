import click
import logging
import random

from jira import JIRA
from datetime import date
from googleapiclient.discovery import build

# internal packages
from ..src import tasklist
from ..src import ticketlist
from ..src import auth

JIRA_SERVER_DEFAULT = 'https://teamprovi.atlassian.net'

INSPIRATIONAL_PHRASES = [
    "have a nice day",
    "carpe diem",
    "go get 'em, tiger",
    "you got this",
    "make it so",
    "get 'er done",
    "that code's not gonna write itself",
    "don't just stand there, let's get to it",
]

@click.command()
@click.option('-e', '--email',
    help='Jira email for authentication(or you can set GTASKS_CHOOSE_EMAIL)')
@click.option('-t', '--jira-token',
    help='Jira API authentication token (or you can set GTASKS_CHOOSE_JIRA_TOKEN)')
@click.option('-s', '--jira-server',
    help=f'Jira server default: {JIRA_SERVER_DEFAULT} (or you can set GTASKS_CHOOSE_JIRA_TOKEN)',
    default=JIRA_SERVER_DEFAULT)
def choose(email, jira_token, jira_server):
    """Lists all current assigned tickets from which to choose, adds them to Google tasks"""

    client = JIRA(server=jira_server, basic_auth=(email, jira_token))
    tl = ticketlist.TicketList(client)

    todo = [] 
    ready = False
    while not ready:
        ticket_keys = __prompt(tl)
        for k in ticket_keys:
            try:
                todo.append(tl.tickets_dict[int(k)])
            except KeyError:
                click.echo(f'There is no {k}\n')
                continue

        if todo:
            click.echo('\nYour choices:')
            for t in todo:
                click.echo(t.display)

            answer = click.prompt('\nAre you sure? [yn]')
            if answer in ['Y', 'y']:
                ready = True
            elif answer in ['N', 'n']:
                todo = []

    today = date.today()

    logging.info('authenticating')
    credentials = auth.authenticate()
    service = build('tasks', 'v1', credentials=credentials)

    tasklist = __make_google_tasklist(service, today.strftime('%m/%d/%Y'))

    for task in todo:
        __make_google_task(service, tasklist['id'], task)

    click.echo(f'Your tasks have been added, {random.choice(INSPIRATIONAL_PHRASES)}!')

def __prompt(ticketlist):
    choices = click.prompt(f'Which ticket(s) do you want to work on today? (comma-separated)\n{ticketlist.prompt}')
    return [i.strip() for i in choices.split(",")]

def __make_google_tasklist(service, tasklist_name):
    try:
        tl = tasklist.get_tasklists(service, tasklist_name)
        logging.debug(f'Tasklist called {tasklist_name} already exists; fetching tasklist')

        results = service.tasklists().get(tasklist=tl[0].id).execute()
        return results
    except IndexError:
        logging.debug('No tasklist for today; creating one now')

    results = service.tasklists().insert(body={'title': tasklist_name}).execute()
    logging.debug(results)

    return results

def __make_google_task(service, tasklist_id, ticket):
    logging.debug(f'creating task {ticket.display}')
    results = service.tasks().insert(
        tasklist=tasklist_id,
        body={'title': ticket.display}
    ).execute()
    logging.debug(f'results: {results}')
