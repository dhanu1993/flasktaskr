import os
import unittest
from project import app, db, bcrypt
from project._config import basedir
from project.models import User 

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False
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
		new_user = User(name=name, email=email, password=bcrypt.generate_password_hash(password))
		db.session.add(new_user)
		db.session.commit()

	def test_users_can_register(self):
		new_user = User("dhanunjaya", "dhanunjaya@flask.com", bcrypt.generate_password_hash("dhanunjaya"))
		db.session.add(new_user)
		db.session.commit()
		test = db.session.query(User).all()
		for t in test:
			t.name
		assert t.name == "dhanunjaya"

	def test_form_is_present_on_login_page(self):
		response = self.app.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Please sign in to access your task list', response.data)
	
	def test_unregistered_user_cannot_login(self):
		response=self.login('dhanunjaya','dhanunjaya')
		self.assertIn(b'Invalid username and password.', response.data)

	def test_registered_user_can_login(self):
		self.register("dhanunjaya", "dhanunjaya@flask.com", "dhanunjaya","dhanunjaya")
		response = self.login("dhanunjaya", "dhanunjaya")
		self.assertIn(b'Welcome!', response.data)

	def test_invalid_form_data(self):
		self.register("dhanunjaya", "dhanunjaya@flask.com", "dhanunjaya", "dhanunjaya")
		response = self.login("hello", "hello")
		self.assertIn(b"Invalid username and password.", response.data)

	def test_form_is_present_on_register_page(self):
		response = self.app.get('/register/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Please register to access the task list.', response.data)

	def test_user_registration(self):
		self.app.get('register/', follow_redirects=True)
		response = self.register('dhanunjaya', "dhanunjaya@flask.com", "dhanunjaya", "dhanunjaya")
		self.assertIn(b"Thanks for registering. please login.", response.data)

	def test_user_registration_error(self):
		self.app.get('register/', follow_redirects=True)
		response = self.register("dhanunjaya", "dhanunjay@flask.com", "dhanunjaya", "dhanunjaya")
		self.app.get('register/', follow_redirects=True)
		response = self.register("dhanunjaya", "dhanunjay@flask.com", "dhanunjaya", "dhanunjaya")
		self.assertIn(b"That username and/or email already exist.", response.data)		

	def test_logged_in_user_can_logout(self):
		self.register("dhanunjaya", "dhanunjaya@flask.com", "dhanunjaya", "dhanunjaya")
		self.login("dhanunjaya", "dhanunjaya")
		response = self.logout()
		self.assertIn(b"Goodbye!", response.data)

	def test_not_logged_in_users_cannot_logout(self):
		response = self.logout()
		self.assertNotIn(b"Goodbye!", response.data)		
	
	def test_default_user_role(self):
		db.session.add(User("dhanunjaya", "dhanunjaya@flask.com", "dhanunjaya"))
		db.session.commit()
		users = db.session.query(User).all()
		print(users)
		for u in users:
			self.assertEqual(u.role, 'user')

if __name__ == '__main__':
	unittest.main()
