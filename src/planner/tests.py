import datetime
from django.urls import reverse
from django.test import TestCase, RequestFactory, LiveServerTestCase
from selenium import webdriver
from users.models import UserProfile, UserManager
from .models import DinnerDecider, TodoList
from .views import LoginView, HomeView, DinnerPlanView, ContactView, AccountView


class PlannerModelsTest(TestCase):
	""" Testing models. """

	def create_user(self):
		"""Creation of a user object."""
		return UserProfile.objects.create(email='test@test.com',
						  first_name='test',
						  last_name='test2',
						  city='testcity',
						  password='password')


	def create_dinner_decider(self, monday='test', 
					tuesday='test', 
					wednesday='test', 
					thursday='test', 
					friday='test',
					saturday='test',
					sunday='test',
					timestamp=datetime.datetime.now()):
		return DinnerDecider.objects.create(Monday=monday, 
						    Tuesday=tuesday,
						    Wednesday=wednesday,
						    Thursday=thursday,
						    Friday=friday,
						    Saturday=saturday,
						    Sunday=sunday,
						    Timestamp=timestamp,
						    User=self.create_user())


	def create_todo_list(self, task='test', date=datetime.datetime.now(), info='test info'):
		return TodoList.objects.create(Task=task, Date=date, Info=info, User=self.create_user())

	
	def test_create_user(self):
		"""Testing the creation of a user."""
		test = self.create_user()
		self.assertTrue(isinstance(test, UserProfile))


	def test_dinner_decider(self):
		""" Testing the creation of a dinner planner."""
		test = self.create_dinner_decider()
		self.assertTrue(isinstance(test, DinnerDecider))
		self.assertEqual(test.__str__(), test.Monday)


	def test_todo_list(self):
		""" Testing the creation of a todo list."""
		test = self.create_todo_list()
		self.assertTrue(isinstance(test, TodoList))
		self.assertEqual(test.__str__(), test.Task)


class PlannerUrlsTest(TestCase):
	""" Testing Urls. """
	
	def create_user(self):
		""" Create a user. """
		return UserProfile.objects.create(email='test@test.com',
									 	  first_name='test',
									      last_name='test2',
									      city='testcity',
									      password='password')


	def test_LandingPage_Url(self):
		""" Testing the landing page URL."""
		response = self.client.get('')
		self.assertEqual(response.status_code, 200)


	def test_SignUpView_Url(self):
		""" Testing the Signup page url."""
		response = self.client.get('/register/')
		self.assertEqual(response.status_code, 200)


	def test_LoginViewView_Url(self):
		""" Testing the login page url."""
		response = self.client.get('/login/')
		self.assertEqual(response.status_code, 200)


	def test_HomeView_Url(self):
		""" Testing the home page url."""
		self.factory = RequestFactory()
		request = self.factory.get('/home/')
		request.user = self.create_user()
		response = HomeView.as_view()(request)
		self.assertEqual(response.status_code, 200)


	def test_DinnerPlanView_Url(self):
		""" Testing the dinner plan creation url."""
		self.factory = RequestFactory()
		request = self.factory.get('/create/')
		request.user = self.create_user()
		response = DinnerPlanView.as_view()(request)
		self.assertEqual(response.status_code, 200)


	def test_AccountView_Url(self):
		""" Testing the account page url."""
		self.factory = RequestFactory()
		request = self.factory.get('/account/')
		request.user = self.create_user()
		response = AccountView.as_view()(request)
		self.assertEqual(response.status_code, 200)

	
	def test_LoginView(self):
		"""Testing the LoginView, post login info to the login path, if return is True, user is logged in."""
		user = self.client.post('/login/', email='test@test.com', password='password')
		self.assertTrue(user)


	def test_LogoutView(self):
		""" If user_logged_out is False the user is logged_out"""
		user = self.client.post('/login/', email='test@test.com', password='password')
		user_logged_out = self.client.logout()
		self.assertFalse(user_logged_out)


	def test_DinnerPLanView_Url(self): 
		""" Testing that users can access the view if they are logged in."""
		self.factory = RequestFactory()
		request = self.factory.get('/enter_plan/')
		request.user = self.create_user()
		response = DinnerPlanView.as_view()(request)
		self.assertEqual(response.status_code, 200)


	def test_DinnerPLanView_non_loggedin(self): 
		"""
		User needs to be logged in for this test to work, if the user isn't logged in it will 
		return a status code 302 (redirect), which it is meant to do for unauthenticated users.
		"""
		response = self.client.get('/create/')
		self.assertRedirects(response, '/?login=/create/')


	def test_contact_view_Url(self):
		""" Testing that ContactView works if you're logged in"""
		self.factory = RequestFactory()
		request = self.factory.get('/contact/')
		request.user = self.create_user()
		response = ContactView.as_view()(request)
		self.assertEqual(response.status_code, 200)


	def test_ContactView_non_loggedin_Url(self):
		""" Testing that ContactView cannot be accessed by non-logged in users"""
		response = self.client.get('/contact/')
		self.assertRedirects(response, '/?login=/contact/')


	def test_ContactLandingView_Url(self):
		""" Contact view accessible by non-registered or non-loggedin users."""
		response = self.client.get('/contact-landing/')
		self.assertEqual(response.status_code, 200)
