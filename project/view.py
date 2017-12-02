from flask import Flask, redirect, url_for, render_template, g, session, flash
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
			return redirect(url_for('main'))
	return render_template("login.html")

