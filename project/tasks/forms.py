from flask_wtf import Form 
from wtforms import StringField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired

#registration form , labels are visible on webpage(Task Name, Due Date, Priority,Status, Username, Email, Password, .....	)
class AddTaskForm(Form):
	task_id=IntegerField()
	name=StringField('Task Name', validators=[DataRequired()])
	due_date = DateField('Due Date (dd/mm/yyyy)', validators=[DataRequired()], format='%d/%m/%Y')
	priority=SelectField('Priority', validators=[DataRequired()], choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10')])
	status=IntegerField('Status')	
