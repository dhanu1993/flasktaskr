import os
import unittest
from views import app, db
from _config import basedir
from models import User 

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir, TEST_DB)
		self.app = app.test_client()
		db.create_all()

	def tearDown(slef):
		db.session.remove()
		db.drop_all()

	def login(self, name, password):
		return self.app.post('/', data=dict(name=name, password=password), follow_redirects=True)
	def register(self, name, email, password, confirm):
		return self.app.post('/register/', data=dict(name=name, email=email, password=password, confirm=confirm), follow_redirects=True)
	def logout(self):
		return self.app.get('logout/', follow_redirects=True)
	def create_user(self, name, email, password):
		new_user = User(name=name, email=email, password=password)
		db.session.add(new_user)
		db.session.commit()
	def create_admin_user(self):
		new_user = User(name="admin123", email="admin123@flask.com", password="admin123", role = "admin")
		db.session.add(new_user)
		db.session.commit()
	def create_task(self):
 		return self.app.post("/add/", data=dict(name="do you work", due_date="1/1/2018", priority='1', posted_date="1/1/2018", status='1'), follow_redirects=True)
	
	def test_logged_in_user_can_access_tasks_page(self):
		self.register("dhanunjaya", "dhanunjaya@flask.com", "dhanunjaya", "dhanunjaya")
		self.login("dhanunjaya", "dhanunjaya")
		response = self.app.get('/tasks/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"Add a new task:", response.data)

	def test_not_logged_in_user_cannot_access_tasks_page(self):
		response = self.app.get("/tasks/", follow_redirects=True)
		self.assertIn(b"You need to login first", response.data)

	def test_user_can_add_tasks(self):
		self.register("dhanunjaya", "dhanunjaya@flask.com", "dhanunjaya", "dhanunjaya")
		self.login("dhanunjaya", "dhanunjaya")
		self.app.get('/tasks/', follow_redirects=True)
		response = self.create_task()
		self.assertIn(b"New entry was successfully posted. Thanks.", response.data)
		
	def test_user_cannot_add_task_when_error(self):
		self.register("dhanunjaya", "dhanunjaya@flask.com", "dhanunjaya", "dhanunjaya")
		self.login("dhanunjaya", "dhanunjaya")
		self.app.get('/tasks/', follow_redirects=True)
		response = self.app.post("/add/", data=dict(name="hello", due_date="", priority="10", posted_date="1/1/2018", status="1"), follow_redirects=True)
		self.assertIn(b"All fields are required.", response.data)

	def test_user_can_complete_tasks(self):
		self.register("dhanunjaya", "dhanunjaya@flask.com", "dhanunjaya", "dhanunjaya")
		self.login("dhanunjaya", "dhanunjaya")
		self.app.get('/tasks/', follow_redirects=True)
		self.create_task()		
		response = self.app.get("/complete/1/", follow_redirects=True)
		self.assertIn(b"The task is complete.", response.data)

	def test_user_can_delete_tasks(self):
		self.register("dhanunjaya", "dhanunjaya@flask.com", "dhanunjaya", "dhanunjaya")
		self.login("dhanunjaya", "dhanunjaya")
		self.app.get('/tasks/', follow_redirects=True)
		self.create_task()		
		response = self.app.get("/delete/1/", follow_redirects=True)
		self.assertIn(b"The task was deleted.", response.data)

	def test_user_cannot_complete_tasks_that_are_not_created_by_them(self):
		self.register("dhanunjaya", "dhanunjaya@flask.com", "dhanunjaya", "dhanunjaya")
		self.login("dhanunjaya", "dhanunjaya")
		self.app.get('/tasks/', follow_redirects=True)
		self.create_task()
		self.logout()
		self.create_user("helloo", "helloo@flask.com", "helloo")
		self.login("helloo", "helloo")
		self.app.get('/tasks/', follow_redirects=True)
		response = self.app.get("/complete/1/", follow_redirects=True)
		self.assertNotIn(b"The task is complete.", response.data)
		self.assertIn(b"You can only update tasks that belong to you.", response.data)
	
	def test_user_cannot_delete_tasks_that_are_not_created_by_them(self):
		self.register("dhanunjaya", "dhanunjaya@flask.com", "dhanunjaya", "dhanunjaya")
		self.login("dhanunjaya", "dhanunjaya")
		self.app.get('/tasks/', follow_redirects=True)
		self.create_task()
		self.logout()
		self.create_user("helloo", "helloo@flask.com", "helloo")
		self.login("helloo", "helloo")
		self.app.get('/tasks/', follow_redirects=True)
		response = self.app.get("/delete/1/", follow_redirects=True)
		self.assertNotIn(b"The task was deleted.", response.data)
		self.assertIn(b"You can only delete tasks that belong to you.", response.data)
	
	def test_admin_user_can_complete_tasks_that_are_not_created_by_them(self):
		self.create_user("dhanunjaya", "dhanunjaya@flask.com", "dhanunjaya")
		self.login("dhanunjaya", "dhanunjaya")
		self.app.get("tasks/" , follow_redirects=True)
		self.create_task()
		self.logout()
		self.create_admin_user()
		self.login("admin123", "admin123")
		self.app.get("/tasks/", follow_redirects=True)
		response = self.app.get("/complete/1/", follow_redirects=True)
		self.assertNotIn(b"You can only update tasks that belong to you.", response.data)

	def test_admin_user_can_delete_tasks_that_are_not_created_by_them(self):
		self.create_user("dhanunjaya", "dhanunjaya@flask.com", "dhanunjaya")
		self.login("dhanunjaya", "dhanunjaya")
		self.app.get("tasks/" , follow_redirects=True)
		self.create_task()
		self.logout()
		self.create_admin_user()
		self.login("admin123", "admin123")
		self.app.get("/tasks/", follow_redirects=True)
		response = self.app.get("/delete/1/", follow_redirects=True)
		self.assertNotIn(b"You can only delete tasks that belong to you.", response.data)
		
if __name__ == '__main__':
	unittest.main()

