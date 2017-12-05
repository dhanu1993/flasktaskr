from views import db
from models import Task
from datetime import date


db.create_all()

db.session.add(Task("Finish this tutorial", date(2017, 12, 5), 10, 1))
db.session.add(Task("Finsh Real Python", date(2017, 12, 5), 10, 1))
db.session.commit()
