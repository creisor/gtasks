#!/usr/bin/env python3

import logging

# for CLI
import click
from .commands import view, choose

#LOGLEVEL = logging.WARN

@click.group(help="A commandline interface to Google Tasks")
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose logging')
def cli(verbose):
    loglevel = logging.DEBUG if verbose else logging.WARN
    logging.basicConfig(
        format='%(asctime)s %(message)s',
        level=loglevel)
    pass

cli.add_command(view.view)
cli.add_command(choose.choose)

def main():
    cli(auto_envvar_prefix='GTASKS')


if __name__ == '__main__':
    main()
