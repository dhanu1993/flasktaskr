from forms import AddTaskForm
from flask import Flask, redirect, url_for, render_template, g, session, flash, request
from functools import wraps
import sqlite3

app = Flask(__name__)

app.config.from_object('_config')

def db_connect():
	return sqlite3.connect(app.config['DATABASE_PATH'])

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash("You need to login first.")
			return redirect(url_for('login'))
	return wrap

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash("Goodbye!")
	return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid credentials. Please try again.'
			return render_template('login.html', error = error)
		else:
			session['logged_in'] = True
			flash("Welcome!")
			return redirect(url_for('tasks'))
	return render_template("login.html")

@app.route('/tasks/')
@login_required
def tasks():
	g.db = db_connect()
	cur=g.db.execute("SELECT name, due_date, priority, task_id FROM tasks WHERE status = 1")
	open_tasks = [dict(name = r[0], due_date=r[1], priority=r[2], task_id=r[3]) for r in cur.fetchall()]
	cur=g.db.execute("SELECT name, due_date, priority, task_id FROM tasks WHERE status = 0")
	closed_tasks = [dict(name = r[0], due_date=r[1], priority=r[2], task_id=r[3]) for r in cur.fetchall()]
	g.db.close()
	return render_template('tasks.html', form=AddTaskForm(request.form), open_tasks=open_tasks, closed_tasks=closed_tasks)

@app.route('/add', methods=['POST'])
@login_required
def new_task():
	g.db=db_connect()
	name=request.form['name']
	due_date = request.form['due_date']
	priority=request.form['priority']
	if not name or not due_date or not priority:
		flash("All field are required. Please try again.")
		return redirect(url_for('tasks'))
	else:
		g.db.execute("INSERT INTO tasks (name, due_date, priority, status) VALUES(?,?,?,1)", [name, due_date, priority])
		g.db.commit()
		g.db.close()
		flash("New entry was successfully posted. Thanks.")
		return redirect(url_for('tasks'))

@app.route('/complete/<int:task_id>')
@login_required
def complete(task_id):
	g.db=db_connect()
	g.db.execute("UPDATE tasks SET status = 0 WHERE task_id="+str(task_id))
	g.db.commit()
	g.db.close()
	flash("The task was mark as complete.")
	return redirect(url_for('tasks'))

@app.route('/delete/<int:task_id>')
@login_required
def delete_entry(task_id):
	g.db=db_connect()
	g.db.execute("DELETE FROM tasks WHERE task_id="+str(task_id))
	g.db.commit()
	g.db.close()
	flash("The task was deleted.")
	return redirect(url_for('tasks'))





































