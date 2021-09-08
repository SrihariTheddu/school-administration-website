from django.shortcuts import (
                  render,
                  redirect
                  )
from Applications.Examination.models import (
          Course,
          TestQuestionPaper,
          TestAnswerSheet,
          Question,
          CourseResult,
          FinalResult,
          CourseQuestions
          )
     
from Applications.Administration.models import Channel
          
from django.core.cache import cache


from django.views.generic import (
      DetailView,
      ListView,
      TemplateView
      )
from django.views.generic.edit import (
      CreateView,
      DeleteView
)
from django.contrib import messages

from Applications.Core.loader import CacheLoader

#students related....

#testanswersheets....       
class TestAnswerSheetListView(ListView,CacheLoader):
	model = TestAnswerSheet
	template_name = 'BlogPage.html'
	context_object_name = 'answersheets'
	
	def get_queryset(self):
		return self.model.objects.filter(uploaded_by=cache.get('channel').username,is_drafted=False)
		
	def get_context_data(self,**kwargs):
	    kwargs=self.load_cache(kwargs)
	    kwargs['drafts']=False
	    kwargs['main_template']='TestAnswersheetListPage.html'
	    kwargs['side_template']='CoursesSideBarPage.html'
	    kwargs['title']='ALL'
	    return super().get_context_data(**kwargs)
	

def CourseTestAnswerSheetListView(request,course_name):
    channel=cache.get('channel')
    answersheets = TestAnswerSheet.objects.filter(uploaded_by=channel.username,course_name=course_name)
    context = {
    'answersheets':answersheets,
    'channel':channel,
    'student':channel,
    'title':'QYZ',
'main_template':'TestAnswersheetListPage.html',
	 'side_template':'CoursesSideBarPage.html'
    }
    return render(request,'BlogPage.html',context)
	    

#url:Exams/tests/all/        
class DraftedAnswerSheetView(ListView,CacheLoader):
	model = TestAnswerSheet
	template_name = 'BlogPage.html'
	context_object_name = 'answersheets'
	
	def get_queryset(self):
		return TestAnswerSheet.objects.filter(uploaded_by=cache.get('channel').username,is_drafted=True)
		
	def get_context_data(self,**kwargs):
	    
	    kwargs=self.load_cache(kwargs)
	    kwargs['drafts']=True
	    kwargs['main_template']='TestAnswersheetListPage.html'
	    kwargs['side_template']='CoursesSideBarPage.html'
	    kwargs['title']='DRAFTS'
	    return super().get_context_data(**kwargs)
	    
class PendingTestAnswerSheetListView(ListView,CacheLoader):
	model = TestAnswerSheet
	template_name = 'BlogPage.html'
	context_object_name = 'answersheets'
	
	def get_queryset(self):
		return self.model.objects.filter(uploaded_by=cache.get('channel').username,is_submitted=False)
		
	def get_context_data(self,**kwargs):
	    
	    kwargs=self.load_cache(kwargs)
	    kwargs['drafts']=False
	    kwargs['title']='PENDING TESTS'
	    kwargs['main_template']='TestAnswersheetListPage.html'
	    kwargs['side_template']='CoursesSideBarPage.html'
	    return super().get_context_data(**kwargs)
	    

class SubmittedTestAnswerSheetListView(ListView,CacheLoader):
	model = TestAnswerSheet
	template_name = 'BlogPage.html'
	context_object_name = 'answersheets'
	
	def get_queryset(self):
		return TestAnswerSheet.objects.filter(uploaded_by=cache.get('channel').username,is_submitted=True)
		
	def get_context_data(self,**kwargs):
	    
	    kwargs=self.load_cache(kwargs)
	    kwargs['drafts']=False
	    kwargs['main_template']='TestAnswersheetListPage.html'
	    kwargs['side_template']='CoursesSideBarPage.html'
	    kwargs['title']='SUBMITTED TESTS'
	    return super().get_context_data(**kwargs)	

	
	
class TestAnswerSheetDetailView(DetailView,CacheLoader):
	model = TestAnswerSheet
	template_name = 'BlogPage.html'
	context_object_name = 'answersheet'
	
	def get_context_data(self,**kwargs):
	    kwargs['testpaper'] = self.object.get_question_paper()
	    kwargs=self.load_cache(kwargs)
	    kwargs['main_template']='TestAnswersheetPage.html'
	    kwargs['side_template']='CoursesSideBarPage.html'
	    return super().get_context_data(**kwargs)




def AddAnswerSheetToDraftView(request,pk):
    answersheet = TestAnswerSheet.objects.get(pk=pk)
    answersheet.is_drafted = True
    answersheet.save()
    messages.add_message(request,20,'Successfully Added to Draft')
    return redirect('Exams:DraftedAnswerSheetsPage')
    
def RemoveAnswerSheetFromDraftView(request,pk):
    answersheet = TestAnswerSheet.objects.get(pk=pk)
    answersheet.is_drafted = False
    answersheet.save()
    messages.add_message(request,20,'Successfully Removed from Draft')
    return redirect('Exams:DraftedAnswerSheetsPage')

	
'''
  Test QuestionPaper Related	
'''
class TestQuestionPaperView(DetailView,CacheLoader):
	model = TestQuestionPaper
	template_name = 'BlogPage.html'
	context_object_name = 'test'
	
	def get_context_data(self,**kwargs):
		answersheet = TestAnswerSheet.objects.get(uploaded_by=cache.get('channel').username,paper_code=self.object.paper_code)
		answersheet.start_exam()
		cache.set('answersheet',answersheet)
		kwargs['answersheet']=answersheet
		kwargs['question_id']=answersheet.attempted_questions[0]
		
		kwargs=self.load_cache(kwargs)
		kwargs['main_template']='TestQuestionPaperPage.html'
		kwargs['side_template']='CoursesSideBarPage.html'
		return super().get_context_data(**kwargs)





'''
-----------------------------------
    TAKE TEST RELATED VIEWS...
'''
class QuestionView(DetailView,CacheLoader):
	model = Question
	template_name = 'MultipleChoiceQuestion.html'
	context_object_name = 'Question'
	
	def get_context_data(self,**kwargs):
	    answersheet = cache.get('answersheet')
	    kwargs['answersheet']=answersheet
	    kwargs['course']=answersheet.get_course()
	    kwargs['questions'] = answersheet.questions
	    
	    kwargs=self.load_cache(kwargs)
	    kwargs['previous']=answersheet.get_previous(self.object.question_code)
	    
	    if len(answersheet.attempted_questions)>0:
	        kwargs['question_id']=answersheet.attempted_questions[0]
	        return super().get_context_data(**kwargs)
	    else:
	        kwargs['question_id']='NO_QUESTION'
	    return super().get_context_data(**kwargs)
	    

#url:Exams/test/python/attempt/1/validate/
def validate(request,pk):
    answersheet = cache.get('answersheet')
    if pk!='NO_QUESTION':
        question= Question.objects.get(pk=pk)
        try:
            response = [question.question_code,request.POST['answer']]
        except:
            response = [question.question_code,False]
        answersheet.post_answer(response)
    else:
       pass 
    if len(answersheet.attempted_questions)>0:
        cache.set('answersheet',answersheet)
        return redirect('Exams:Question-DetailView',pk=answersheet.attempted_questions[0])
        
    else:
        answersheet.update()
        cache.set('answersheet',answersheet)
        return redirect('Exams:TestReviewPage',pk=answersheet.serials[0])

        
#url:Exams/tests/python/review/   
class TestReviewView(DetailView,CacheLoader):
    model = Question
    template_name = 'BlogPage.html'
    
    def get_context_data(self,**kwargs):
        answersheet = cache.get('answersheet')
        kwargs['answersheet']=answersheet
        kwargs['questions']=answersheet.questions
        
        kwargs=self.load_cache(kwargs)
        kwargs['main_template']='TestDetailsPage.html'
        kwargs['side_template']='CoursesSideBarPage.html'
        return super().get_context_data(**kwargs)

#url:Exams/tests/python/submit/     
def TestSubmitView(request,pk):
    answersheet = cache.get('answersheet')
    answersheet.submit()
    return redirect('Exams:TestAnswerSheet-DetailView',pk=answersheet.pk)
    
    def get_context_data(self,**kwargs):
        
        kwargs=self.load_cache(kwargs)
        return super().get_context_data(**kwargs)   
                
#url:Exams/tests/python/result/    
class TestResultView(DetailView,CacheLoader):
    model = TestAnswerSheet
    template_name = 'BlogPage.html'
    context_object_name = 'answersheet'
    
    def get_context_data(self,**kwargs):
        
        kwargs=self.load_cache(kwargs)
        kwargs['main_template']='TestResult.html'
        kwargs['side_template']='CoursesSideBarPage.html'
        return super().get_context_data(**kwargs)
       
'''
------------------------------------
      STUDENT RESULTS PAGE
'''       
class StudentResultView(DetailView,CacheLoader):
	model = FinalResult
	template_name = 'StudentResultPage.html'
	context_object_name = 'result'
	
	def get_context_data(self,**kwargs):
	    
	    kwargs=self.load_cache(kwargs)
	    kwargs['standard_courses']=Course.objects.filter(standard=cache.get('channel').standard)
	    return super().get_context_data(**kwargs)



''''
------------------------------------
     STAFF RELTED VIEWS....
'''
class PostTestPaperCreateView(TemplateView,CacheLoader):
    template_name = 'PostTestPaperPage.html'
    
    def get_context_data(self,**kwargs):
        course=cache.get('course')
        kwargs['questions']=CourseQuestions.objects.all()
        kwargs=self.load_cache(kwargs)
        kwargs['course']=course
        code=course.course_code+str(cache.get('channel').admission_number)+str(TestQuestionPaper.objects.count())
        cache.set('code',code)
        kwargs['code']=code
        
        kwargs=self.load_cache(kwargs)
        return super().get_context_data(**kwargs)
        
    def post(self,request):
        course=cache.get('course')
        code=cache.get('code')
        
        
        
        testpaper = TestQuestionPaper(
       course_questions=CourseQuestions.objects.get(pk=int(request.POST['question'])),
        paper_code=code,
        duration=request.POST['duration'],
        message=request.POST['message'],
        no_of_questions=0,
        max_marks=0
        )
        testpaper.save()
        return redirect('Exams:StaffPostedTestDetailPage',pk=testpaper.pk)



class StaffPostedTestListView(DetailView,CacheLoader):
    model = Course
    template_name = 'StaffBlogPage.html'
    context_object_name = 'course'
    
    
    def get_context_data(self,**kwargs):
        
        cache.set('course',self.object)
        try:
            cq=CourseQuestions.objects.get(course=self.object)
            kwargs['tests']=TestQuestionPaper.objects.filter(course_questions=cq)
        except:
            kwargs['tests']=[]
        
        kwargs=self.load_cache(kwargs)
        kwargs['main_template']='StaffPostedTestListPage.html'
        
        return super().get_context_data(**kwargs)
        

class StaffPostedTestDetailView(DetailView,CacheLoader):
    model = TestQuestionPaper
    template_name = 'StaffBlogPage.html'
    context_object_name = 'test'
    
    def get_context_data(self,**kwargs):
        
        
        kwargs=self.load_cache(kwargs)
        kwargs['main_template']='StaffPostedTestDetailPage.html'
        return super().get_context_data(**kwargs)
        

def PostedTestDeleteView(request,pk):
    TestQuestionPaper.objects.get(pk=pk).delete()
    return redirect('Exams:StaffPostedTestListPage',pk=cache.get('course').pk)
    		
		        
class StaffSubmittedAnswerSheetsListView(DetailView,CacheLoader):
    model = TestQuestionPaper
    template_name = 'StaffBlogPage.html'
    context_object_name='testpaper'
    
    
    def get_context_data(self,**kwargs):
        
        kwargs['answersheets']=TestAnswerSheet.objects.filter(paper_code=self.object.paper_code)
        
        kwargs=self.load_cache(kwargs)
        kwargs['main_template']='StaffSubmittedAnswerSheetListPage.html'
        return super().get_context_data(**kwargs)
        
        
class ResultLoginView(TemplateView,CacheLoader):
	template_name = 'LoginPage.html'
	
	def get_context_data(self,**kwargs):
		kwargs['title']='RESULT LOGIN PAGE'
		return super().get_context_data(**kwargs)
	
	def post(self,request):
		username = request.POST['username']
		password = request.POST['password']
		try:
			channel = Channel.objects.get(username=username)
			return redirect('Exams:StudentExamResultPage',pk=channel.pk)
		except:
			messages.add_message(request,20,'NO USER FOUND....')
			return redirect('Exams:ResultLoginPage')
			
			
class StaffPostCourseQuestionView(TemplateView,CacheLoader):
	template_name = 'StaffPostCourseQuestionsPage.html'
	
	
	
	def get_context_data(self,**kwargs):
		kwargs=self.load_cache(kwargs)
		
		kwargs['courses'] = Course.objects.filter(incharge=cache.get('channel'))
		return super().get_context_data(**kwargs)
		
		
	def post(self,request):
		course = Course.objects.get(pk=request.POST['course'])
		from Applications.Core.exams import ParseQuestions,ParseCourseQuestions
		from DataProcessorSystem.FixturesInstallation.questions import QUESTIONS
		try:
			questions = ParseQuestions(course,QUESTIONS)
			cq = ParseCourseQuestions(course,questions)
			messages.add_message(request,20,f"COURSE QUESTIONS CREATED  CODE:{cq}")
		except:
			messages.add_message(request,20,'COULD NOT CREATE COURSE QUESTIONS')
		return redirect('Exams:StaffPostTestCreatePage')


class StaffCourseQuestionsDetailView(DetailView,CacheLoader):
	model = CourseQuestions
	template_name = 'StaffBlogPage.html'
	context_object_name = 'coursequestions'
	
	def get_context_data(self,**kwargs):
		kwargs=self.load_cache()
		
		kwargs['main_template']='StaffCourseQuestionsDetailPage.html'
		cache.set('cq',self.object)
		return super().get_context_data(**kwargs)
		
class StaffCourseQuestionsListView(DetailView,CacheLoader):
	model = Course
	template_name = 'StaffBlogPage.html'
	context_object_name = 'cscqs'
	
	
	
	
	
	def get_context_data(self,**kwargs):
		kwargs=self.load_cache(kwargs)
		
		kwargs['cqs']=CourseQuestions.objects.filter(course=self.object)
		kwargs['main_template']='StaffCourseQuestionsListPage.html'
		return super().get_context_data(**kwargs)
		
def StaffCourseQuestionsDeleteView(request,pk):
	cq = CourseQuestions.objects.get(pk=pk)
	cq.delete()
	messages.add_message(request,20,'COURSE QUESTIONS DELETED SUCCESSFULLY')
	return redirect('Exams:StaffCourseQuestionsListPage',pk=cache.get('course').pk)


class StudentExamResultView(DetailView,CacheLoader):
    model = Channel
    template_name = 'StudentExamResultPage.html'
    context_object_name = 'channel'
    
    def get_context_data(self,**kwargs):
        course_results = CourseResult.objects.filter(student=self.object)
        courses = []
        for course_result in course_results:
            courses.append(course_result.course.course_name)
        from DataProcessorSystem.GoogleSheetProcessor.DataBaseModel import DataBaseModel
        from mysite.siteconf import (
		GOOGLE_SPREADSHEET_NAME,
		CREDENTIALS_PATH
		)
        db = DataBaseModel(GOOGLE_SPREADSHEET_NAME,CREDENTIALS_PATH)
        db.setprimarykey('ID')
        marks = db.getvalues(self.object.username,courses)
        result=[]
        for index,course in enumerate(courses):
            result.append([course,marks[index]])
        kwargs['result']=result
        return super().get_context_data(**kwargs)
			

def StaffQuestionDeleteView(request,pk):
    question = Question.objects.get(pk=pk)
    question.delete()
    messages.add_message(request,20,"QUESTION DELETED SUCCESSFULLY")
    return redirect('Exams:StaffCourseQuestionsDetailPage',pk=cache.get('cq').pk)

