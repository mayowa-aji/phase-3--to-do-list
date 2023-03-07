import click
import os
from colorama import init, Fore, Back, Style
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    task_name = Column(String)
    priority = Column(String)

    def __repr__(self):
        return f'Task(id={self.id}, task_name="{self.task_name}", priority="{self.priority}")'

engine = create_engine('sqlite:///todo.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

os.system('cls' if os.name=='nt' else 'clear')
@click.group()
def cli():
    pass

@click.command()
def welcome():
    message = '''

  wWw  wWw   .-.     wWw  wWw         \/        .-.  (o)__(o)    (o)__(o)\ \  // wW  Ww oo_
  (O)  (O) c(O_O)c   (O)  (O)        (OO)     c(O_O)c(__  __)    (__  __)(o)(o) (O)(O)/  _)-<
  ( \  / ),'.---.`,  / )  ( \      ,'.--.)   ,'.---.`, (  )        (  )  ||  ||  (..) \__ `.
   \ \/ // /|_|_|\ \/ /    \ \    / /|_|_\   / /|_|_|\ \ )(          )(   |(__)|   ||     `. |
    \o / | \_____/ || \____/ |    | \_.--.  | \_____/ |(  )        (  )  /.--.\  _||_    _| |
   _/ /  '. `---' .`'. `--' .`    '.   \) \ '. `---' .` )/          )/  -'    `-(_/\_),-'   |
  (_.'     `-...-'    `-..-'        `-.(_.'   `-...-'  (           (                 (_..--'

    '''
    click.echo(Fore.CYAN + Back.BLACK+ message)

@click.command()
@click.argument('task')
@click.option('-p', '--priority', type=int, default=1, help='Priority level of the task')
@click.option('-l', '--priority-levels', type=click.Choice(['low', 'medium', 'high']), default='low', help='Dictionary of priority levels')
def add(task, priority, priority_levels):
    """Add a task to the to-do list"""
    priority_dict = {
        'low': {1: 'low', 2: 'medium', 3: 'high'},
        'medium': {1: 'medium', 2: 'high', 3: 'urgent'},
        'high': {1: 'high', 2: 'urgent', 3: 'critical'}
    }
    priority_level = priority_dict[priority_levels][priority]
    new_task = Task(task_name=task, priority=priority_level)
    session.add(new_task)
    session.commit()
    click.echo(f'{Fore.YELLOW + Back.BLACK}Task "{task}" added to to-do list with priority level "{priority_level}".')

@click.command()
@click.argument('task_id', type=int)
def delete(task_id):
    """No longer need to do it be  DONE it """
    task = session.query(Task).get(task_id)
    if task:
        session.delete(task)
        session.commit()
        click.echo(f'Task "{task.task_name}" deleted from to-do list.')
    else:
        click.echo(f'Invalid task ID: {task_id}')

@click.command()
@click.option('-p', '--priority', type=click.Choice(['tuple', 'list', 'dict']), default='tuple', help='Type of priority list')
def show(priority):
    """Let me see what I have to do """
    tasks = session.query(Task).order_by(Task.priority).all()
    for task in tasks:
        click.echo(Fore.YELLOW + Back.BLACK + f'Priority: [{task.priority}]  {task.task_name}')

# cli.add_command(welcome)
cli.add_command(add)
cli.add_command(delete)
cli.add_command(show)

if __name__ == '__main__':
    cli()
