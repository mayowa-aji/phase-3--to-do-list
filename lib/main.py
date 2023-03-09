import click
import os
from colorama import init, Fore, Back, Style
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

commands = ["""
**********************************************************************************

        "add -[Hint] - Use underscore instead of spaces between words"

        "delete -[Hint] - Use the index of the task you would like to delete"

        "display -[Hint] - Displays all tasks"

**********************************************************************************
  """]
CONTEXT_SETTINGS = dict(help_options_names= ['-h', '--help'])


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    task_name = Column(String)
    priority = Column(String)

    def __repr__(self):
        return f'Task(id={self.id}, task_name="{self.task_name}", priority="{self.priority}")'

class QuitHandler:
    def __init__(self,is_quit=False):
        self._is_quit = is_quit
    @property
    def is_quit(self):
        return self._is_quit
    @is_quit.setter
    def is_quit(self, value):
        self._is_quit = value

engine = create_engine('sqlite:///todo.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
quithandler = QuitHandler()

Base.metadata.create_all(engine)

os.system('cls' if os.name=='nt' else 'clear')

@click.group()
def cli():
    pass

def welcome():
    message = '''

  
 __   __  _______  __   __    _______  _______  _______    _______  __   __  ___   _______    __  
|  | |  ||       ||  | |  |  |       ||       ||       |  |       ||  | |  ||   | |       |  |  | 
|  |_|  ||   _   ||  | |  |  |    ___||   _   ||_     _|  |_     _||  |_|  ||   | |  _____|  |  | 
|       ||  | |  ||  |_|  |  |   | __ |  | |  |  |   |      |   |  |       ||   | | |_____   |  | 
|_     _||  |_|  ||       |  |   ||  ||  |_|  |  |   |      |   |  |       ||   | |_____  |  |__| 
  |   |  |       ||       |  |   |_| ||       |  |   |      |   |  |   _   ||   |  _____| |   __  
  |___|  |_______||_______|  |_______||_______|  |___|      |___|  |__| |__||___| |_______|  |__| 



   Welcome to YOU GOT THIS!! An application that allows you to organize your day by creating, listing and deleting completed tasks. ENJOY!!

    '''
    click.echo(Fore.CYAN + Back.BLACK+ message)
    click.echo("Please select one of the below commands to proceed:")
    for cmd in commands:
        click.echo(cmd)

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
    task = task.split("_")
    task = " ".join(task)
    print(task)
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
def display(priority):
    """Let me see what I have to do """
    tasks = session.query(Task).order_by(Task.priority).all()
    for task in tasks:
        click.echo(Fore.GREEN + Back.BLACK + f'Priority: [{task.priority}]  {task.task_name}')



@click.command()
def run():
    welcome()
    while quithandler.is_quit == False:
      cmd = click.prompt("Please enter a command to proceed",  type=str)
      split_text = cmd.split()
      try:
          cli(split_text)
      except SystemExit:
          pass


@click.command()
def quit():
    quithandler.is_quit = True
    os.system('cls' if os.name=='nt' else 'clear')
    click.echo('''
    
 __   __  _______  __   __  _______    _______    _______  ______    _______  _______  _______    ______   _______  __   __  __  
|  | |  ||   _   ||  | |  ||       |  |   _   |  |       ||    _ |  |       ||   _   ||       |  |      | |   _   ||  | |  ||  | 
|  |_|  ||  |_|  ||  |_|  ||    ___|  |  |_|  |  |    ___||   | ||  |    ___||  |_|  ||_     _|  |  _    ||  |_|  ||  |_|  ||  | 
|       ||       ||       ||   |___   |       |  |   | __ |   |_||_ |   |___ |       |  |   |    | | |   ||       ||       ||  | 
|       ||       ||       ||    ___|  |       |  |   ||  ||    __  ||    ___||       |  |   |    | |_|   ||       ||_     _||__| 
|   _   ||   _   | |     | |   |___   |   _   |  |   |_| ||   |  | ||   |___ |   _   |  |   |    |       ||   _   |  |   |   __  
|__| |__||__| |__|  |___|  |_______|  |__| |__|  |_______||___|  |_||_______||__| |__|  |___|    |______| |__| |__|  |___|  |__| 
''')

cli.add_command(add)
cli.add_command(delete)
cli.add_command(display)
cli.add_command(quit)

if __name__ == '__main__':
    run()
