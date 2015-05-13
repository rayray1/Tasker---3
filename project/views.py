# project/views.py - The Controller -  Contains business logic e.g routing rules

# imports
from forms import AddTaskForm, RegisterForm, LoginForm

from functools import wraps
from flask import Flask, flash, redirect, render_template, \
 	request, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import datetime


# config
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import Task, User

# login required decorater
def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap


# route handlers


#login function
@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			user = User.query.filter_by(name=request.form['name']).first()
			if user is not None and user.password == request.form['password']:
				session['logged_in'] = True
				session['user_id'] = user.id
				session['role'] = user.role
				flash('Welcome!')
				return redirect(url_for('tasks'))
			else:
				error = 'Invalid username or password'
		# else:
		# 	error = 'Both fields are required.'
	return render_template('login.html', form=form, error=error)







# logout function
@app.route('/logout/')
@login_required
def logout():
	session.pop('logged_in', None)
	session.pop('user_id', None)
	session.pop('role', None)
	flash('Goodbye')
	return redirect(url_for('login'))



# tasks function - querying the db for open & closed tasks
@app.route('/tasks/')
@login_required
def tasks():
	open_tasks = db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())
	closed_tasks = db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())
	return render_template(
		'tasks.html',
		form=AddTaskForm(request.form),
		open_tasks=open_tasks,
		closed_tasks=closed_tasks
	)



# Add new tasks
@app.route('/add/', methods=['GET', 'POST'])
@login_required
def new_task():
	error = None
	form = AddTaskForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_task = Task(
				form.name.data,
				form.due_date.data,
				form.priority.data,
				datetime.datetime.utcnow(), # captures current date n passes it to Tasks() class
				'1',
				session['user_id']
			)
			db.session.add(new_task)
			db.session.commit()
			flash('New entry was successfully posted. Thanks.')
			return redirect(url_for('tasks'))
		else:
			return render_template('tasks.html', form=form, error=error)
	return render_template('tasks.html', form=form, error=error)



# mark tasks as complete
@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
	new_id = task_id
	task = db.session.query(Task).filter_by(task_id=new_id)
	if session['user_id'] == task.first().user_id or session['role'] == "admin":
		task.update({"status": "0"})
		db.session.commit()
		flash('The task was marked as complete.')
		return redirect(url_for('tasks'))
	else:
		flash('You can only update tasks that belong to you.')
		return redirect(url_for('tasks'))



# delete tasks
@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
	new_id = task_id
	task = db.session.query(Task).filter_by(task_id=new_id)
	if session['user_id'] == task.first().user_id or session['role'] == "admin":
		task.delete()
		db.session.commit()
		flash('The task was deleted')
		return redirect(url_for('tasks'))
	else:
		flash('You can only delete tasks that belong to you')
		return redirect(url_for('tasks'))




# register function
@app.route('/register/', methods=['GET', 'POST'])
def register():
	error = None
	form = RegisterForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit(): # returns True or False depending on data submitted
			new_user = User(
				form.name.data,
				form.email.data,
				form.password.data,
			)
			try:
				db.session.add(new_user)
				db.session.commit()
				flash('Thanks for registering. Please Login.')
				return redirect(url_for('login'))
			except IntegrityError:
				error = 'That username and/or email already exists.'
				return render_template('register.html', form=form, error=error)
	return render_template('register.html', form=form, error=error)



# error flashing
def flash_errors(form):
	for field, errors in form.errors.items():
		for error in errors:
			flash(u"Error in the %s field - %s" %(
				getattr(form, field).label.text, error), 'error')

