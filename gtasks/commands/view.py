import click

from ..src import tasklist

@click.command()
@click.option('-y', '--yesterday', is_flag=True, help='See yesterday\'s tasks')
@click.option('-a', '--all-tasks', is_flag=True, help='See tasks from all tasklists')
def view(yesterday, all_tasks):
    """Allows you to view tasks in your list(s)"""

    if all_tasks:
        print(f'view all tasks')
    elif yesterday:
        print(f'view yesterday')
    else:
        print(f'view today')
