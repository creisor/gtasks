import logging

from functools import cached_property


class Ticket(object):
    def __init__(self, ticket, is_subtask=False):
        self.__ticket = ticket
        self.is_subtask = is_subtask

    @property
    def key(self):
        return self.__ticket.key

    @property
    def summary(self):
        return self.__ticket.fields.summary

    @property
    def display(self):
        return f'{self.key}: {self.summary}'

    @property
    def subtasks(self):
        return self.__ticket.fields.subtasks

class TicketList(object):
    def __init__(self, jira_client):
        self.jira_client = jira_client
        self.query = 'assignee is not EMPTY and assignee = currentUser() AND project = DEVOPS AND status in (Blocked, "To Do", "In Progress", "In Review") AND type not in (Epic, Subtask) order by created DESC'
        self.__active_statuses = ['to do', 'blocked', 'in progress', 'in review']

    @cached_property
    def tickets(self):
        logging.debug(f'running search: {self.query}')
        results = self.jira_client.search_issues(self.query,  fields=['summary', 'subtasks', 'status'])

        tickets = []
        for ticket in results:
            tickets.append(Ticket(ticket))
            for subtask in ticket.fields.subtasks:
                if subtask.fields.status.name.casefold() in self.__active_statuses:
                    tickets.append(Ticket(subtask, is_subtask=True))

        return tickets

    @property
    def tickets_dict(self):
        return dict(zip(range(1, len(self.tickets)+1), self.tickets))

    @property
    def prompt(self):
        string = ''
        for k,v in self.tickets_dict.items():
            string += f'{k}) '
            if v.is_subtask:
                string += ' ' * 2
            string += f'{v.display}\n'

        return string
