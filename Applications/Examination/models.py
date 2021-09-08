''' 
   EXAMINATION APPLICATION
'''

from django.db import models

from django.shortcuts import render

from django.urls import reverse,reverse_lazy


from Applications.Education.models import (
        Course
        )
        
from Applications.Management.models import Report


from django.contrib import messages


from Applications.Administration.models import (Channel)

from django.db.models.signals import (    post_save,
     pre_save,
     pre_delete,
     post_delete,
     pre_init,
     post_init,
     
     )
     
from django.core.signing import Signer

#Just a model reference to use as global
class ParseQuestion(models.Model):
    pass
   
        
        
#url:Exams/Question/form/        
class Question(models.Model):
	
	course = models.ForeignKey(
	Course,
	on_delete=models.CASCADE,
	null=True,
	related_name='course_questions'
	)
	
	is_script = models.BooleanField(default=False)
	
	is_blank = models.BooleanField(default=False)
	
	is_choice = models.BooleanField(default=False)
	
	question_code = models.CharField(max_length=10,unique=True,primary_key=True)
	
	question= models.TextField(
	max_length=500)
	
	option1  = models.CharField(
	max_length=100,blank=True,null=True)
	
	option2  = models.CharField(
	max_length=100,blank=True,null=True)
	
	option3  = models.CharField(
	max_length=100,blank=True,null=True)
	
	option4  = models.CharField(
	max_length=100,blank=True,null=True)
	
	answer = models.CharField(
	max_length=500)
	
	marks = models.IntegerField()
	
	def __str__(self):
		return self.question_code
		
	#validating the answer....	
	def validate(self,answer):
		if self.is_choice and self.answer==answer:
			return self.marks
		if self.is_script:
			return self.marks-1
			
			
		
		

		
#url:Exams/Coursequestions/form/
class CourseQuestions(models.Model):
	
	course = models.ForeignKey(
	Course,
	on_delete = models.CASCADE,
	related_name='course_questions_set')
	
	questions = models.ManyToManyField(
	Question,
	blank=True)
	
	
	
	def __str__(self):
		return self.course.course_name
		
	def add(self,question):
	    self.questions.add(question)
		


#url:Exams/TestQuestionPaper/form/
class TestQuestionPaper(models.Model):
	
	course_questions = models.ForeignKey(
	CourseQuestions,
	on_delete=models.CASCADE,
	related_name='course_tests')
	
	paper_code = models.CharField(
	max_length=10,unique=True,primary_key=True)
	

	duration = models.FloatField()
	
	no_of_questions = models.IntegerField()
	
	max_marks = models.IntegerField()
	
	uploaded_on = models.DateTimeField(auto_now=True)
	
	message = models.TextField(
	max_length=300,blank=True)
	
	answersheets = models.ManyToManyField(
	'TestAnswerSheet',
	blank=True)
	
	reports = models.ManyToManyField(
	Report,
	blank=True)
	
	
	
	#returning string
	def __str__(self):
		return self.course_questions.course.course_name+' to '+str(self.course_questions.course.standard.standard)
	
	def get_absolute_url(self):
	    return reverse('Education:StaffCourseDetailPage',pk=self.object.course_questions.course.pk)
	
	#getting all answersheets	
	def get_answersheets(self):
		return TestAnswerSheet.objects.filter(paper_code=self.paper_code)
	
	#submitting answersheet individually by student	
	def submit(self,answersheet):
	    self.answersheets.add(answersheet)
	    return None
	
	#getting question count   
	def get_question_count(self):
	    return len(self.course_questions.questions.all())
	
	def get_total_marks(self):
		total_marks = 0
		for question in self.course_questions.questions.all():
			total_marks += question.marks
		return total_marks
			
			
	
	#parsing the questions    
	def parse_questions(self):
	    parser_questions = []
	    for index,question in enumerate(self.course_questions.questions.all()):
	        pq = ParseQuestion()
	        pq.code = question.question_code
	        pq.number = index
	        pq.attempted = False
	        parser_questions.append(pq)
	    return parser_questions
	    
	#getting serializers
	def get_serializers(self,**kwargs):
		serializers = []
		for question in self.course_questions.questions.all():
			serializers.append(question.question_code)
		return serializers
	
	#getting key	
	def get_key(self):
		key = {}
		for question in self.course_questions.questions.all():
			key[question.question_code]=[question.answer,question.marks]
		return key	    

	
#Creating Answersheet for every individual student using credentials
def test_question_before_save(instance,sender,**kwargs):
    instance.max_marks = instance.get_total_marks()
    
 			
def test_question_after_save(instance,sender,**kwargs):
    
	for student in instance.course_questions.course.standard.standard_students.all():
		answersheet = TestAnswerSheet(
		paper_code=instance.paper_code,
		uploaded_by = student.username,
		credentials = student.username+instance.paper_code,
		is_submitted=False,
		answers=" ",
		score=0,
		grade="0",
		show_result =True,
		course_name=instance.course_questions.course.course_name
		).save()
	from Applications.DashBoard.models import (Notification,Reminder)
	Notification(
	standard=instance.course_questions.course.standard,
	sender=instance.course_questions.course.incharge,
	code='NT'+str(instance.course_questions.course.standard.standard)+str(Notification.objects.count()),
	message=f'''Course Incharge has posted the new Quiz
	Your Last Date for submission of Assifnment is {instance.uploaded_on}.
	Submit your Test intime and incovenience.
	
	''',
	title='Quiz TestPosted').save()
	Reminder(
	sender=instance.course_questions.course,
	code='RM'+str(instance.course_questions.course.course_code)+str(Reminder.objects.count()),
	message=f'''Course Incharge has posted the new Assignment Document.
	Your Last Date for submission of Assifnment is {instance.uploaded_on}.
	Submit your Assignment intime and incovenience.
	
	''',
	title=instance.course_questions.course.course_name+' Test Posted ',
	last_date=instance.uploaded_on).save()
	from Applications.Main.models import StaffChannelContent
	StaffChannelContent.objects.get(username=instance.course_questions.course.incharge.username).posted_tests.add(instance)
		
		
		
post_save.connect(test_question_after_save,TestQuestionPaper)

pre_save.connect(test_question_before_save,TestQuestionPaper)	

#url:Exams/TestAnswerSheet/form/	
class TestAnswerSheet(models.Model):
    
	
	paper_code = models.CharField(
	max_length=10)
	
	course_name = models.CharField(
	max_length=100)
		
	#channel_username+papercode
	credentials = models.CharField(max_length=100,unique=True)
	
	uploaded_by = models.CharField(max_length=100)
	
	answers = models.TextField(
	max_length=300,blank=True)
	
	is_submitted = models.BooleanField(default=False)
	
	submitted_on = models.DateTimeField(auto_now=True)
	
	score = models.IntegerField(default=0)
	
	show_result = models.BooleanField(default=False)
	
	grade = models.CharField(max_length=4,blank=True)
	
	is_drafted = models.BooleanField(default=False,editable=True)
	
	#returning string...
	def __str__(self):
		return self.course_name+' is uploaded by '+self.uploaded_by
		

	
	#getting question paper
	def get_question_paper(self):
	    try:
	        return TestQuestionPaper.objects.get(paper_code=self.paper_code)
	    except:
	        return 'No paper'
	#get course name	
	def get_course(self):
		return self.get_question_paper().course_questions.course.course_name
	
	#startExam >>> 	
	def start_exam(self,**kwargs):
		self.questions = self.get_question_paper().parse_questions()
		self.load_questions()
		self.my_answers = {}
		self.serials=self.get_question_paper().get_serializers()
		self.is_cycled = False
		
	#loading questions....	
	def load_questions(self,**kwargs):
		self.attempted_questions = []
		for single_list in self.questions:
			self.attempted_questions.append(single_list.code)
			
	#getting previous questions
	def get_previous(self,key):
	    for question in self.questions:
	        if question.code==key:
	            previous = question.number
	            break
	    if previous!=1 and previous==0:
	        return self.serials[previous-1]
	    else:
	        return self.serials[1]  
	#posting answer		
	def post_answer(self,answer):
	    if answer[1]:
	        self.my_answers[answer[0]]=answer[1]
	    else:
	        self.my_answers[answer[0]]='NA'
	    for question in self.questions:
	        if question.code==answer[0]:
	           self.questions[question.number].attempted=True
	    return self.clear_question(answer[0])
	
	#clearing the question formdb
	def clear_question(self,key):
	    try:
	        self.attempted_questions.remove(key)
	        return key
	    except:
	        return key
	#updating the answers       
	def update(self):
	    self.answers=self.my_answers
	    self.is_submitted = False
	    self.save()
	#submitting the answersheet	
	def submit(self,**kwargs):
		self.answers=self.answers
		self.is_submitted = True
		self.save()
		self.evaluate()
		self.save()
	#no of questions attempted	
	def no_of_questions_attempted(self):
	    return len(self.answers.split(','))
	
	#validating answersheet
	def evaluate(self,**kwargs):
	    print('Evaluation started')
	    answers = dict(self.answers)
	    key_set = self.get_question_paper().get_key()
	    print(key_set)
	    score = 0
	    for key,value in answers.items():
	        print(key)
	        if key_set[key][0]==value:
	            score += key_set[key][1]
	            print(score)
	    self.score = score
	    self.grade = self.get_grade(score)
	    
	
	    
		
	def get_grade(self,score,**kwargs):
	    _grade = (score/self.get_question_paper().max_marks)*100
	    if _grade<35:
	        return 'F'
	    elif _grade<50:
	        return 'D'
	    elif _grade<60:
	        return 'C'
	    elif _grade<70:
	        return 'B'
	    elif _grade<80:
	        return 'A'
	    elif _grade<90:
	        return 'OS'
	    else:
	        return 'NA'
	        
	        
	        
		
		
		
	        
			
		
		
#url:Exams/CourseResult/form/
class CourseResult(models.Model):
	
	course = models.ForeignKey(
	Course,
	on_delete = models.CASCADE,
	related_name='course_results')

	
	student = models.ForeignKey(
	Channel,
	on_delete = models.CASCADE,
	related_name='registered_courses')
	
	key = models.CharField(max_length=10,unique=True)
	
	internal_marks = models.IntegerField()
	
	external_marks = models.IntegerField()
	
	total_marks = models.IntegerField()
	
	grade = models.CharField(max_length=10)
	
	percentage = models.FloatField()
	
	passed = models.BooleanField(default=False)
	
	present_marks = models.IntegerField()
	
	def __str__(self):
		return self.student.username+' of ' + self.course.course_name
		
	def save(self,**kwargs):
	    signer = Signer()
	    self.key = signer.sign(self.course.course_name+self.student.username)
	    try:
	        super().save()
	        FinalResult.objects.get(student=self.student).add(self)
	    except:
	        pass
		
	def register(self,credentials):
	    self.student = credentials['student']
	    self.internal_marks=credentials['internal marks']
	    self.external_marks=credentials['external marks']
	    self.total_marks=credentials['total marks']
	    self.grade=credentials['grade']
	    self.percentage=credentials['percentage']
	    self.passed=credentials['passed']
	    self.course = credentials['course']
	    self.present_marks = 0
	    try:
	        if self.student.standard==self.course.standard:
	            self.save()
	            
	            return True
	        else:
	            
	            return False
	    except:
	        return False
	    
		

#url:Exams/FinalResult/form/
class FinalResult(models.Model):
	
	student = models.OneToOneField(
	Channel,
	on_delete = models.CASCADE,
	related_name = 'channel_progress_card')
	
	courses_result = models.ManyToManyField(
	CourseResult,blank=True)
	
	percentage = models.FloatField(blank=True,null=True)
	
	gpa = models.FloatField(blank=True,null=True)
			
	is_promoted = models.BooleanField(default=False)
	
	def __str__(self):
		return self.student.username
		
	def add(self,course,flag=True):
	    for this_course in self.courses_result.all():
	        if this_course==course:
	            flag=False
	            break
	    if flag:
	        self.courses_result.add(course)

	