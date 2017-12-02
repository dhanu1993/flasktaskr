import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
	cursor = connection.cursor()
	cursor.execute("CREATE TABLE tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, due_date TEXT NOT NULL, priority INTEGER NOT NULL, status INTEGER NOT NULL)")
	cursor.execute("INSERT INTO tasks(name, due_date, priority, status) VALUES('Finish this tutorial', '2/12/2017', 10, 1)")	
	cursor.execute("INSERT INTO tasks(name, due_date, priority, status) VALUES('Real Python Course ', '2/12/2017', 10, 1)")	
