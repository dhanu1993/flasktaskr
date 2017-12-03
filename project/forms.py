from flask_wtf import Form 
from wtforms import StringField, DateField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired

class AddTaskForm(Form):
	task_id = IntegerField()
	name = StringField('Task Name', validators=[DataRequired()])
	due_date = DateField('Due Date (mm/dd/yyyy)', validators=[DataRequired()], format='%m/%d/%Y' )
	priority = IntegerField('Priority', validators=[DataRequired()])
	status = IntegerField('Status')