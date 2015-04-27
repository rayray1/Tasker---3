# project/db_create.py - Sets up & creates the database

import sqlite3
from config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:

	# get a cursor object to execute SQL commands
	c = connection.cursor()

	# create table
	c.execute("""CREATE TABLE tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL, due_date TEXT NOT NULL, priority INTEGER NOT NULL, status INTEGER NOT NULL)""")

	# insert dummy data into table
	c.execute(
		'INSERT INTO tasks (name, due_date, priority, status)'
		'VALUES("Finish my assignment", "05/20/2014", 10, 1)'
	)

	c.execute(
		'INSERT INTO tasks (name, due_date, priority, status)'
		'VALUES("Play Basketball", "05/20/2014", 10, 1)'
	)