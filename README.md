THE TO-DO LIST

Our Project is CLI tool that can be used to manage a to-do list.  The to-do list has incorporated several modules, to incude "click", "os", "colorama" and "sqlalchemy".

The "click package" is used to create command'line interfaces. The "os" is the operating system.
The "colorama" was used to color the text.
Lastly we used SQLalchemy to interact with the database using ORM approach.

We have a class called Task that inherits from 'declarative_base()'.
The class defines the structure of the table in a SQLlite database. The table has three colums: 'id', 'task_name' and 'priority'. 

Then we have a database engine using the `create_engine()`function from SQLalchemy.

We also defined four functions using @click.command decorator. 
The functions includes welcome, add, delete and show.

The welcome() function welcomes you with welcome word art.
The add() function adds a new task to the database.
The delete() function deletes and task you have completed.
The show() function shows all the task and it's priority level. 



