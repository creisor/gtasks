#!/usr/bin/env python3

# for CLI
import click
from .commands import view

@click.group(help="A commandline interface to Google Tasks")
def cli():
    pass
cli.add_command(view.view)

def main():
    cli()


if __name__ == '__main__':
    main()
