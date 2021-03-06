from flask import Flask, redirect, url_for, render_template, session, request, flash, Blueprint
from functools import wraps
from sqlalchemy.exc import IntegrityError 

import datetime 

from .forms import AddTaskForm
from project import db
from project.models import Task

tasks_blueprint = Blueprint('tasks', __name__)

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash("You need to login first")
			return redirect(url_for('users.login'))
	return wrap

def open_tasks():
	return db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())
def closed_tasks():
	return db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())

@tasks_blueprint.route("/tasks/")
@login_required
def tasks():
	return render_template('tasks.html',form=AddTaskForm(request.form), open_tasks=open_tasks(), closed_tasks=closed_tasks(), name=session['name'])	

@tasks_blueprint.route('/add/', methods=['POST'])
@login_required
def new_task():
	error=None
	form = AddTaskForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			import datetime
			new_task=Task(form.name.data, form.due_date.data, form.priority.data, datetime.datetime.utcnow(),'1', session['user_id'])
			db.session.add(new_task)
			db.session.commit()
			flash("New entry was successfully posted. Thanks.")
			return redirect(url_for('tasks.tasks'))
		else:
			flash("All fields are required.")
			return render_template('tasks.html', form=form, error=error)
	return render_template('tasks.html', form=form, error=error)

@tasks_blueprint.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
	new_id = task_id
	task = db.session.query(Task).filter_by(task_id = new_id)
	if session['user_id'] == task.first().user_id or session['role'] == "admin":
		task.update({"status":"0"})
		db.session.commit()
		flash("The task is complete.")
		return redirect(url_for('tasks.tasks'))	
	else:
		flash("You can only update tasks that belong to you.")
		return redirect(url_for('tasks.tasks'))

@tasks_blueprint.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
	new_id=task_id
	task = db.session.query(Task).filter_by(task_id=new_id)
	
	if session['user_id'] == task.first().user_id or session['role'] == 'admin':
		task.delete()
		db.session.commit()
		flash("The task was deleted.")
		return redirect(url_for('tasks.tasks'))
	else:
		flash("You can only delete tasks that belong to you.")
		return redirect(url_for('tasks.tasks'))

@tasks_blueprint.route("/pending/<int:task_id>/")
@login_required
def pending(task_id):
	new_id = task_id
	task = db.session.query(Task).filter_by(task_id=new_id)

	if session['user_id'] == task.first().user_id or session['role'] == 'admin':
		task.update({"status":"1"})
		db.session.commit()
		flash("The task is reopened.")
		return redirect(url_for('tasks.tasks'))
	else:
		flash("You can only update tasks that belongs to you.")
		return redirect(url_for('tasks.tasks'))

