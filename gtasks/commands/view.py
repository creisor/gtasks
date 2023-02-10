import click

@click.command()
@click.option('--yesterday', is_flag=True, help='See yesterday\'s tasks')
def view(yesterday):
    if yesterday:
        print(f'view yesterday')
    else:
        print(f'view today')
