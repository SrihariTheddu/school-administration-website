from django.test import (TestCase,Client)

from django.template.context_processors import request

#import views

# Create your tests here.
class TestClass(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		pass
	
	def setUp(self):
		self.client = Client()
		
	def tearDown(self):
		pass
		
	def test_chunk_content(self):
		self.assertEqual(views.get_chunk_code('Web Devolpment'),'WD')
		self.assertEqual(views.get_chunk_code('Python'),'PY')
		self.assertEqual('Android Devolpment Course','ADC')
		
	def test_application_status(self):
		response = self.client.get('application/status/')
		self.assertEquals(response.status,200)
		self.assertRedirects(response,"")
		
	def test_search_application(self):
		application_id = 1
		self.assertRedirects(views.SearchApplicationView().as_view(),f'application/{application_id}/status/')
		
	def test_application_delete_view(self):
		response = self.client.get('applications/1/delete')
		self.assertRedirects(response.status_code,200)
	
	def test_course_delete_view(self):
		self.assertRedirects(views.ManagerCourseDeleteView(request,1).as_view(),'manager/courses/all/')
		
	def test_manager_approve_admission_view(self):
		self.assertRedirects(views.ManagerApproveAdmissionView(),f'manager/admissions/all/')