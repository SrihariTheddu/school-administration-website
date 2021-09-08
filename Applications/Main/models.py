''' 
   MAIN APPLICATION
'''
from django.db import models

from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    MinValueValidator,
    MaxValueValidator
    )
    
from Applications.Education.models import (
        AssignmentDocument,
        PostTutorial,
        PostAssignment,
        Course
        )
from Applications.DashBoard.models import (
          Notification,
          Circular,
          Reminder,
          IndividualMessage
          )
          
          

from Applications.Examination.models import (TestAnswerSheet,TestQuestionPaper)

from django.core.cache import cache

from Applications.Management.models import Event


class BasicContent(models.Model):
    
    username = models.CharField(max_length=40,unique=True)
    
    key = models.CharField(
	max_length=100,unique=True)
	
    standard = models.IntegerField()
    
    notifications = models.ManyToManyField(
	Notification,
	blank=True,
	)
	
    circulars = models.ManyToManyField(
	Circular,
	blank=True,
	)
	
    reminders = models.ManyToManyField(
	Reminder,
	blank=True,
	)
	
    events = models.ManyToManyField(
	Event,
	blank=True,
	)
	
    individual_messages = models.ManyToManyField(
	IndividualMessage,
	blank=True,
	)
	
    #df_notifications = models.ManyToManyField(
#	Notification,
#	blank=True,
#	related_name='my_df_notifications')
#	
#    df_circulars = models.ManyToManyField(
#	Circular,
#	blank=True,
#	related_name='my_df_circulars')
#	
#    df_reminders = models.ManyToManyField(
#	Reminder,
#	blank=True,
#	related_name='my_df_reminders')
#	
#    df_events = models.ManyToManyField(
#	Event,
#	blank=True,
#	related_name='my_df_events')
#	
#    df_individual_messages = models.ManyToManyField(
#	IndividualMessage,
#	blank=True,
#	related_name='my_df_im')
#	
	
	
	
    class Meta:
        abstract = True
	
    def __str__(self):
        return self.username
        
       
		
		
    def change_password(self,new_password):
	    self.password = new_password
	    
    def authenticate(self,query_password):
	    return self.password==query_password
	    
	    
    def get_standard(self):
    	'''
    	***
    	GETTING THE STANDARD
    	***
    	'''
    	return self.get_channel().standard
	
    def get_channel(self):
	    from Applications.Administration.models import Channel
	    return Channel.objects.get(username=self.username)
	    
    def get_draft_box(self):
	    queryset = []
	    for set in Circular.objects.all():
	        queryset.append(set)
	    for set in Notification.objects.filter(standard=self.get_standard()):
	        queryset.append(set)
	    for set in self.reminders.all():
	        queryset.append(set)
	    return queryset

    def get_all_inbox(self):
	    queryset = []
	    for set in self.reminders.all():
	        queryset.append(set)
	    for set in self.circulars.all():
	        queryset.append(set)
	    for set in self.notifications.all():
	        queryset.append(set)
	    for set in self.individual_messages.all():
	        queryset.append(set)
	    return queryset
	    
	   
	    
		
	
	
    
    

class ChannelContent(BasicContent):
	
	
	tutorials = models.ManyToManyField(
	PostTutorial,blank=True)
	
	
	answersheets = models.ManyToManyField(
	TestAnswerSheet,
	blank=True)
	
	assignments = models.ManyToManyField(
	AssignmentDocument,
	blank=True)
	
	
	
	
	
	def get_registered_courses(self):
		'''
		***
		GETTING THE REGISTERED COURSES
		***
		'''
		return self.get_channel().registered_courses()
	    
	def get_post_assignments(self):
		'''
		***
		GETTING THE POSTED ASSIGNMENTS
		***
		'''
		posted_assignments = []
		for course in self.get_registered_courses():
			posted_assignments.append(course.get_course_assignments())
		return posted_assignments
	    
	def get_assignment_documents(self):
		'''
		***
		GETTING THE ASSIGNMENT DOCS
		***
		'''
		return self.get_channel().assignment_documents.all()
	    
	    
	def get_submitted_assignments(self):
		'''
		***
		GETTING THE SUBMITTED ASSIGNMENT DOCS
		***
		'''
		return self.get_channel().assignment_documents.filter(is_submitted=True)
	    
	def get_pending_assignments(self):
		'''
		***
		GETTING THE PENDING ASSIGNMENT DOCS
		***
		'''
		return self.get_channel().assignment_documents.filter(is_submitted=False)
	    
	def get_drafted_assignments(self):
		'''
		***
		GETTING THE DRAFTED ASSIGNMENT DOCS
		***
		'''
		return self.get_channel().assignment_documents.filter(is_drafted=True)
	    	   
	def get_posted_tutorials(self):
		'''
		***
		GETTING THE POST TUTORIALS
		'''
		return self.tutorials.all()
	    
		

class StaffChannelContent(BasicContent):
    
	
    courses = models.ManyToManyField(
    Course,
    blank=True)
    
    
    posted_assignments = models.ManyToManyField(
    PostAssignment,
    blank=True)
    
    posted_tests = models.ManyToManyField(
    TestQuestionPaper,
    blank=True)
    
    posted_tuttorials = models.ManyToManyField(
    PostTutorial,
    blank=True)
    
    leave_letters =  models.ManyToManyField(
    'LeaveForm',
    blank=True)
    
    def __str__(self):
        return self.username
        
    def get_courses(self):
        return self.courses.all()
        
    def get_posted_assignments(self):
        return self.posted_assignments.all()
        
    def get_posted_tests(self):
        return self.posted_tests.all()
    def get_assignments_of(self,course):
        return self.posted_assignments.filter(course=course)
        
    def get_tests_of(self,course):
        from Applications.Examination.models import CourseQuestions
        try:
            course_questions=CourseQuestions.objects.get(course=course)
            return self.posted_tests.filter(course_questions=course_questions)
        except:
            return None
            
     
        		

class LeaveForm(models.Model):
    
    channelcontent = models.ForeignKey(
    ChannelContent,
    on_delete=models.CASCADE,
    related_name='leave_form'
    )
    
    reason=models.TextField(max_length=400,blank=True)
    
    from_date = models.DateField(auto_now=False)
    
    to_date = models.DateField(auto_now=False)
    
    is_granted = models.BooleanField(
    default=False)
    
    applied_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.channelcontent.username
        
        
class StaffLeaveForm(models.Model):
    
    channelcontent = models.ForeignKey(
    StaffChannelContent,
    on_delete=models.CASCADE
    )
    
    reason=models.TextField(max_length=400,blank=True)
    
    from_date = models.DateField(auto_now=False)
    
    to_date = models.DateField(auto_now=False)
    
    is_granted = models.BooleanField(
    default=False)
    
    applied_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.channelcontent.username
        
    def save(self):
        super().save()
        from Applications.Administration.models import (Channel,Standard)
        standard=Standard.objects.get(standard=self.channelcontent.standard)
        incharge=Channel.objects.get(standard=standard,is_staff=True)
        StaffChannelContent.objects.get(username=incharge.username).leave_letters.add(self)



class Settings(models.Model):
	
	KEY = models.CharField(
	max_length=20,
	default = '#h@&!%2000{}*^~\theddu',
	unique = True
	)
	
	ADMIN = models.CharField(
    max_length=50)
    
	PASSWORD = models.CharField(
    max_length=14
    )
    
	RESULTS_SESSION = models.BooleanField(default=False)
    
	ADMISSIONS_SESSION = models.BooleanField(default=False)
    
	GOOGLE_SHEET_NAME = models.CharField(max_length=50,null=True,blank=True)
    
	GOOGLE_SHEET_CREDENTIALS_PATH = models.FilePathField()
    
	CLEAR_DATABASE = models.BooleanField(default=False)
    
	def __str__(self):
		return self.ADMIN
        
        
        
        

        
 
    
    

    
		
	