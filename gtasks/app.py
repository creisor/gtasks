#!/usr/bin/env python3

import click
from .commands import view

@click.group(help="A commandline interface to Google Tasks")
def main():
    pass

main.add_command(view.view)

if __name__ == '__main__':
    main()
