#!/usr/bin/env python3

from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']


def main():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('tasks', 'v1', credentials=creds)

        # Call the Tasks API
        results = service.tasklists().list(maxResults=30).execute()
        items = results.get('items', [])

        if not items:
            print('No task lists found.')
            return

        print('Task lists:')
        for item in items:
            print(u'{0} ({1})'.format(item['title'], item['id']))
            t = service.tasks().list(tasklist=item['id'], showCompleted=True, showDeleted=True, showHidden=True).execute()
            if t['items']:
                for task in t['items']:
                    msg = ''
                    try:
                        if task['deleted']:
                            msg += '[COMPLETED] '
                    except KeyError:
                        pass
                    if task['title']:
                        msg += f'"{task["title"]}"'
                        print(msg)
            else:
                print(f'No tasks found for {item["title"]}')
            print()

    except HttpError as err:
        print(err)

if __name__ == '__main__':
    main()
