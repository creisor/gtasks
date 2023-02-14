import click

# internal packages
from ..src import tasklist

@click.command()
@click.option('-y', '--yesterday', is_flag=True, help='See yesterday\'s tasks')
@click.option('-a', '--all-tasks', is_flag=True, help='See tasks from all tasklists')
def view(yesterday, all_tasks):
    """Allows you to view tasks in your list(s)"""

    tasklists = tasklist.get_tasklists()
    print(tasklists)
    import pdb; pdb.set_trace()

    if all_tasks:
        print('view all')
    elif yesterday:
        print('view yesterday')
    else:
        print('view today')
