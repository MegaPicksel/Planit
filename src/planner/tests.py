import datetime
import time
from django.urls import reverse
from django.test import TestCase, RequestFactory, LiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from users.models import UserProfile, UserManager
from .models import DinnerDecider, TodoList
from .views import LoginView, HomeView, DinnerPlanView, TodayAjaxView, AjaxTodoView, ContactView, AccountView
from .forms import LoginForm, DinnerDeciderForm, TodoForm, ContactForm


class PlannerModelsTest(TestCase):
	""" Testing models. """

	@staticmethod
	def create_user():
		"""Creation of a user object."""
		User = get_user_model()
		return User.objects.create_user('test@test.com', 'password')


	@staticmethod
	def create_dinner_decider(monday='test', 
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
										    User=PlannerModelsTest.create_user())


	@staticmethod
	def create_todo_list(task='test', date=datetime.datetime.now(), info='test info'):
		return TodoList.objects.create(Task=task, Date=date, Info=info, User=PlannerModelsTest.create_user())

	
	def test_create_user(self):
		"""Testing the creation of a user."""
		test = PlannerModelsTest.create_user()
		self.assertTrue(isinstance(test, UserProfile))


	def test_dinner_decider(self):
		""" Testing the creation of a dinner planner."""
		test = PlannerModelsTest.create_dinner_decider()
		self.assertTrue(isinstance(test, DinnerDecider))
		self.assertEqual(test.__str__(), test.Monday)


	def test_todo_list(self):
		""" Testing the creation of a todo list."""
		test = PlannerModelsTest.create_todo_list()
		self.assertTrue(isinstance(test, TodoList))
		self.assertEqual(test.__str__(), test.Task)


class PlannerUrlsTest(TestCase):
	""" Testing Urls. """

	def test_LandingPage_Url(self):
		""" Testing the landing page URL."""
		response = self.client.get('')
		self.assertEqual(response.status_code, 200)


	def test_SignUpView_Url(self):
		""" Testing the Signup page url."""
		response = self.client.get('/register/')
		self.assertEqual(response.status_code, 200)


	def test_LoginView_Url(self):
		""" Testing the login page url."""
		response = self.client.get('/login/')
		self.assertEqual(response.status_code, 200)


	def test_HomeView_Url(self):
		""" Testing the home page url."""
		self.factory = RequestFactory()
		request = self.factory.get('/home/')
		request.user = PlannerModelsTest.create_user()
		response = HomeView.as_view()(request)
		self.assertEqual(response.status_code, 200)


	def test_HomeView_Url_not_loggedin(self):
		""" Not logged in"""
		response = self.client.get('/home/')
		self.assertRedirects(response, '/?login=/home/')


	def test_AccountView_Url(self):
		""" Testing the account page url."""
		self.factory = RequestFactory()
		request = self.factory.get('/account/')
		request.user = PlannerModelsTest.create_user()
		response = AccountView.as_view()(request)
		self.assertEqual(response.status_code, 200)


	def test_DinnerPlanView_Url(self): 
		""" DinnerPlanView if logged in."""
		self.factory = RequestFactory()
		request = self.factory.get('/enter_plan/')
		request.user = PlannerModelsTest.create_user()
		response = DinnerPlanView.as_view()(request)
		self.assertEqual(response.status_code, 200)


	def test_DinnerPlanView_Url_non_loggedin(self): 
		""" Not logged in. """
		response = self.client.get('/create/')
		self.assertRedirects(response, '/?login=/create/')


	def test_TodayAjaxView_Url(self):
		""" AjaxTodoView if logged in."""
		self.factory = RequestFactory()
		request = self.factory.get('/today/')
		request.user = PlannerModelsTest.create_user()
		response = ContactView.as_view()(request)
		self.assertEqual(response.status_code, 200)


	def test_TodayAjaxView_Url_non_loggedin(self):
		""" Not logged in."""
		response = self.client.get('/today/')
		self.assertRedirects(response, '/?login=/today/')


	def test_AjaxTodoView_Url(self):
		""" AjaxTodoView if logged in."""
		self.factory = RequestFactory()
		request = self.factory.get('/todo/')
		request.user = PlannerModelsTest.create_user()
		response = ContactView.as_view()(request)
		self.assertEqual(response.status_code, 200)


	def test_AjaxTodoView_Url_non_loggedin(self):
		""" Not logged in."""
		response = self.client.get('/todo/')
		self.assertRedirects(response, '/?login=/todo/')


	def test_contact_view_Url(self):
		""" ContactView if logged in. """
		self.factory = RequestFactory()
		request = self.factory.get('/contact/')
		request.user = PlannerModelsTest.create_user()
		response = ContactView.as_view()(request)
		self.assertEqual(response.status_code, 200)


	def test_ContactView_non_loggedin_Url(self):
		""" Not logged in. """
		response = self.client.get('/contact/')
		self.assertRedirects(response, '/?login=/contact/')


	def test_ContactLandingView_Url(self):
		""" Contact view accessible by non-registered or non-loggedin users."""
		response = self.client.get('/contact-landing/')
		self.assertEqual(response.status_code, 200)


class PlannerFormsTest(TestCase):
	""" Testing forms."""

	def test_LoginForm(self):
		""" Test LoginForm."""
		user = PlannerModelsTest.create_user()
		data = {'username': 'test@test.com', 'password': 'password'}
		form = LoginForm(data=data)
		self.assertTrue(form.is_valid())


	def test_DinnerDeciderForm(self):
		""" Test Dinner Decider form."""
		plan = PlannerModelsTest.create_dinner_decider()
		data = {'Monday': plan.Monday, 'Tuesday': plan.Tuesday, 'Wednesday': plan.Wednesday,
				'Thursday': plan.Thursday, 'Friday': plan.Friday, 'Saturday': plan.Saturday,
				'Sunday': plan.Sunday}
		form = DinnerDeciderForm(data=data)
		self.assertTrue(form.is_valid())


	def test_TodoForm(self):
		""" Test Todo list form"""
		todo = PlannerModelsTest.create_todo_list()
		data = {'Task': todo.Task, 'Date': todo.Date, 'Info': todo.Info}
		form = TodoForm(data)
		self.assertTrue(form.is_valid()) 


	def test_ContactForm(self):
		""" Testing Contact form."""
		user = PlannerModelsTest.create_user()
		data = {'Name': 'John', 'Message': 'test message', 'Email': 'test2@test.com', 'user': user}
		form  = ContactForm(data=data)
		self.assertTrue(form.is_valid())


class SeleniumTests(LiveServerTestCase):
	"""
	Selenium is used for testing the apps functionality in the browser.
	Running Selenium tests with Chrome. To run tests in another browser the specific web driver for 
	the browser must be installed. The web driver must also be on the path, or the path to the 
	web driver must be explicity stated, as is the case here.
	"""
	@classmethod
	def setUpClass(cls):
		
		super().setUpClass()
		cls.selenium = webdriver.Chrome(executable_path='C:\chromedriver.exe')


	@classmethod
	def tearDownClass(cls):
		
		cls.selenium.quit()
		super().tearDownClass()


	def test_LoginView_Selenium(self):
		"""
		Testing the login view. Use live_server_url instead of typing in the development url, 
		the webdriver will open the site on a different url because it'll open on a different port.
		"""
		user = PlannerModelsTest.create_user()
		self.selenium.get(self.live_server_url +'/login/')
		self.selenium.refresh()
		username = self.selenium.find_element_by_name("username").send_keys("test@test.com")
		password = self.selenium.find_element_by_name("password").send_keys("password")
		button = self.selenium.find_element_by_id("form-button").click()
		time.sleep(2)


	def test_SignUpView_Selenium(self):
		""" Testing browser functionality of SingUpView. """
		self.selenium.get(self.live_server_url + '/register/')
		email = self.selenium.find_element_by_name("email").send_keys("email@email.com")
		first_name = self.selenium.find_element_by_name("first_name").send_keys("test")
		city = self.selenium.find_element_by_name("city").send_keys("New York")
		password1 = self.selenium.find_element_by_name("password1").send_keys("password1")
		password2 = self.selenium.find_element_by_name("password2").send_keys("password1")
		button = self.selenium.find_element_by_id("form-button").click()
		user = UserProfile.objects.all()
		self.assertEqual(user[0].email, "email@email.com")		# Assert that a user was added to the database.
		self.assertEqual(user[0].first_name, "test")
		time.sleep(2)


	def test_LogoutView(self):
		# Login First
		user = PlannerModelsTest.create_user()
		self.selenium.get(self.live_server_url +'/login/')
		self.selenium.refresh()
		username = self.selenium.find_element_by_name("username").send_keys("test@test.com")
		password = self.selenium.find_element_by_name("password").send_keys("password")
		button = self.selenium.find_element_by_id("form-button").click()
		# Logout
		logout = self.selenium.find_element_by_id("logout").click()
		time.sleep(2)