from django.test import TestCase

import views

# Create your tests here.

class TestClass(TestCase):
	
	def setUp(self):
		pass
		
	def tearDown(self):
		pass
		
	def test_is_registered_course(self):
		self.assertEqual(views.CourseDetailView().is_registered(),True)
		
		
	def test_search_course_view(self):
		self.assertEqual(views.SearchCourseView('Python'),True)
		self.assertEqual(views.SearchCourseView('Chinese'),False)
	
	
	def test_course_list_view(self):
		pass


