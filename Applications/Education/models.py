''' 
   EDUCATION APPLICATION
'''

from django.db import models

from Applications.Administration.models import (
               Channel,
               Standard,
               )
from Applications.Management.models import (Report)

from django.db.models.signals import (    post_save,
     pre_save,
     pre_delete,
     post_delete,
     pre_init,
     post_init
     )

from django.core.signing import Signer

import datetime

from django.core.cache import cache

from django.shortcuts import redirect

from django.urls import reverse


'''
method defined as the gloabal
'''
def get_chunk_code(title):
    chunk_list = title.split(' ')
    if len(chunk_list)==1:
        return title[0:2].upper()
    else:
        chunk_content = ''
        for index,chunk in enumerate(chunk_list):
            chunk_content+=chunk[0].upper()
            if index>3:
                break
        return chunk_content



class Course(models.Model):
	
	course_name = models.CharField(
	max_length=100)
	
	course_code = models.CharField(
	max_length=6)
	
	incharge = models.ForeignKey(
	Channel,
	on_delete=models.CASCADE,
	related_name='channel_courses')
	
	standard = models.ForeignKey(
	Standard,
	on_delete=models.CASCADE,
	related_name= 'standard_courses')
	
	outcomes = models.TextField(
	max_length=1000
	)
	
	content = models.OneToOneField(
	'Content',
	on_delete = models.CASCADE,
	null=True)
	
	
	
	def __str__(self):
		return self.course_name
		
	def get_incharge(self,**kwargs):
	    '''
	    returning the channel
	    '''
	    return self.incharge
	    
	    
	def save(self):
		'''
		***
		CREATING THE CHANNEL CONTENT
		***
		'''
		content = Content(
	    course_name=self.course_name,
	    references='#'
	    )
		content.save()
		self.content = content
		super().save()
		
		self.incharge.get_channel_content().courses.add(self)
	    
	def get_course_units(self):
		return self.course_units.all()
		
	def get_course_tutorials(self):
		return self.course_tutorials.all()
	
	
	def get_course_assignments(self):
		return self.course_assignments.all()
		
		
	def get_registered_students(self):
		'''
		returning the registered
		students 
		'''
		registered_stds = []
		course_results =  self.course_results.all()
		for cr in course_results:
			registered_stds.append(cr.student)
		return registered_stds
		
	def get_course_results(self):
		return self.course_results.all()
		
	def get_course_tests(self):
		return self.course_tests.all()
		
	def get_course_reminders(self):
		return self.course_reminders.all()
		
	def get_course_questions(self):
		return self.course_questions.all()
		
	def get_course_questions_set(self):
		return self.course_questions_set.all()
			
#-----------------------------------
#Content		
class Content(models.Model):
	
	course_name = models.CharField(
	max_length=100)
	
	references = models.TextField(max_length=300,editable=True)
	
	units = models.ManyToManyField(
	'Unit',blank=True)
	
	posted_tutorials = models.ManyToManyField(
	'PostTutorial',blank=True)
	
	
	def __str__(self):
		return self.course_name
	
		
	def get_course_units(self):
		return self.content_units.all()
		
#-----------------------------------
#Unit	
class Unit(models.Model):
	
	course = models.ForeignKey(
	Course,
	on_delete = models.CASCADE,null=True,
	related_name='course_units'
	)
	
	this_content = models.ForeignKey(
	Content,
	on_delete = models.CASCADE,null=True,
	related_name='content_units'
	)
	
	code = models.CharField(max_length=10,primary_key=True)
	
	title = models.CharField(max_length=150)
	
	introduction = models.TextField(max_length=500,blank=True)
	
	information = models.FileField(
	upload_to='uploads/',
	max_length=300,blank=True,null=True)
	
	practice_questions = models.TextField(max_length=1000,blank=True,null=True)
	
	summary = models.TextField(max_length=1000,blank=True,null=True)
	
	def __str__(self):
		return self.title
		
	def save(self):
		super().save()
		'''
		adding the content
		'''
		Content.objects.get(pk=self.this_content.pk).units.add(self)
	
	def parse_summary(self):
		'''
		parsing the summary
		'''
		return list(self.summary.split(','))
		
	def parse_practice_questions(self):
		'''
		parsing the practice questioms
		
		'''
		return list(self.practice_questions.split('?'))
		
	def parse_to_text(self):
		'''
		parsing to the text
		'''
		with open(self.information.path,'r') as file:
			pdf = file.read()
		return pdf
	    
	def get_course(self,**kwargs):
	    return self.course
	    
	def download(self,**kwargs):
		'''
		downloading the unit
		'''
		with open(f'downloads/{self.title}.pdf','w') as writer:
			with open(self.information.path) as reader:
				writer.write(reader.read)
		return writer
	    
	def parse_text_in_doc(self):
		content = []
		ph_1 = self.parse_to_text().split(';')
		for text in ph_1:
			inner_text = text.split(':')
			content.append(inner_text[0],inner_text[1])
		return content
	    

	        
		
		
#-----------------------------------
#PostAssignment		
class PostAssignment(models.Model):
	
	code = models.CharField(max_length=20,unique=True)
	
	course = models.ForeignKey(
	Course,
	on_delete = models.CASCADE,
	related_name='course_assignments')
	
	title = models.CharField(
	max_length=50,unique=True)
	
	question = models.TextField(
	max_length=500)
	
	message = models.TextField(
	max_length=500,blank=True)
	
	due_date = models.DateTimeField(auto_now=False)
	
	reports = models.ManyToManyField(
	Report,
	blank=True)
	
	def __str__(self):
		return self.title
	
	def get_absolute_url(self,**kwargs):
	    return redirect('Education:StaffCourseDetailPage',pk=self.object.course.pk)
		
def post_assignment_before_save(instance,sender,**kwargs):
    import random as r
    instance.code = instance.course.course_code+str(instance.course.standard.standard)+str(PostAssignment.objects.count())+str(r.randint(100,999))
	
	
def post_assignment_after_save(instance,sender,**kwargs):
	for student in instance.course.standard.standard_students.all():
	    assignment = AssignmentDocument(
	      qas = instance,
		  code=instance.code,
		  credentials=student.username+instance.code,
		  uploaded_by=student,
		  course_name=instance.course.course_name,
		  is_submitted=False
		  ).save()
	from Applications.DashBoard.models import (Notification,Reminder)
	Notification(
	standard=instance.course.standard,
	sender=instance.course.incharge,
	code='NT'+str(instance.course.standard.standard)+str(Notification.objects.count())+str(get_chunk_code(instance.title)),
	message=f'''{instance.course.incharge.username} has posted the new Assignment Document of {instance.title} for the course {instance.course.course_name}.
	Your Last Date for submission of Assifnment is {instance.due_date}.
	Submit your Assignment intime and incovenience.
	Follow the Instructions provided in the document.
	     **** ALL THE BEST ****
	
	''',
	title=f'Assignment Posted from {instance.course.course_name}').save()
	Reminder(
	sender=instance.course,
	code='RM'+str(instance.course.standard.standard)+str(Notification.objects.count())+str(get_chunk_code(instance.title)),
	message=f'''{instance.course.incharge.username} has posted the new Assignment Document of {instance.title} for the course {instance.course.course_name}.
	Your Last Date for submission of Assifnment is {instance.due_date}.
	Submit your Assignment intime and incovenience.
	Follow the Instructions provided in the document.
	     **** ALL THE BEST ****
	
	''',
	title=f'Assignment Posted from {instance.course.course_name}',
	last_date=instance.due_date).save()
	from Applications.Main.models import StaffChannelContent
	StaffChannelContent.objects.get(username=instance.course.incharge.username).posted_assignments.add(instance)
		  
def post_assignment_after_delete(instance,sender,**kwargs):
	assignments = AssignmentDocument.objects.filter(code=instance.code)
	for assignment in assignments:
		assignment.delete()
	
pre_save.connect(post_assignment_before_save,sender=PostAssignment)
		  
post_save.connect(post_assignment_after_save,sender=PostAssignment)
	
post_delete.connect(post_assignment_after_delete,sender=PostAssignment)
	
		
		
class AssignmentDocument(models.Model):
	
	qas = models.ForeignKey(
	PostAssignment,
	on_delete=models.CASCADE,
	related_name='submissions')
	
	code = models.CharField(max_length=20)
	
	#channel_username+assignmentcode
	credentials = models.CharField(max_length=100,unique=True)
	
	uploaded_by = models.ForeignKey(
	Channel,
	on_delete=models.CASCADE,
	related_name='assignment_documents')
	
	document = models.FileField(
	upload_to='uploads/',
	max_length=500,blank=True,null=True)
	
	is_submitted = models.BooleanField(default=False)
	
	uploaded_on = models.DateTimeField(auto_now=True)
	
	course_name = models.CharField(
	max_length=50)
	
	is_drafted = models.BooleanField(default=False,editable=True)
	
	def __str__(self):
		return self.course_name+' uploaded by '+self.uploaded_by.username
		
	def submit_document(self):
	    try:
	        if self.document.path is not None:
	            self.is_submitted = True
	            self.save()
	            self.flag = True
	    except:
	        self.flag=False
	        
		
	def get_course(self):
	    return self.qas.course.course_name
	    
	
	    
	def is_open(self):
		'''
		checking if the work is open
		Thank You
		'''
		last_date = self.qas.due_date.date()
		now = datetime.date.today()
		delta = last_date-now
		print(delta)
		if now<last_date:
			return True
		else:
			return False
		
	
	def submit(self,document,**kwargs):
		'''
		submitting the document
		'''
		self.document = document
		self.submit_document()
		
		
class PostTutorial(models.Model):
	
	course = models.ForeignKey(
	Course,
	on_delete = models.CASCADE,
	related_name='course_tutorials')
	
	title = models.CharField(
	max_length=150)	
	
	description = models.CharField(
	max_length=150)	
	
	information = models.FileField(
	upload_to='uploads/',
	max_length=300,blank=True,null=True)
	
	reports = models.ManyToManyField(
	Report,
	blank=True)
	
	def __str__(self):
		return self.title
		
		

		
def post_tutorial_after_save(instance,sender,**kwargs):
	'''
	Adding Tutorials to all cc
	
	'''
	for channel in instance.course.get_registered_students():
		channel.get_channel_content().tutorials.add(instance)
	'''
	sending notification to atds
	'''	
	from Applications.DashBoard.models import (Notification)
	Notification(
	standard=instance.course.standard,
	sender=instance.course.incharge,
	code='NT'+str(instance.course.standard.standard)+str(Notification.objects.count()),
	message=f'''{instance.course.incharge.username} has posted the new Tutorial of {instance.title} for the course {instance.course.course_name}.
	Follow the Instructions provided in the document.
	     **** ALL THE BEST ****
	
	''',
	title=f'Tutorial Posted from {instance.course.course_name}').save()
	
		

post_save.connect(post_tutorial_after_save,sender=PostTutorial)

	
			