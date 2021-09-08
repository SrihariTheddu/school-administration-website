from django.shortcuts import (
                   render,
                   redirect
                   )
                   
from django.urls import reverse

from Applications.Education.models import (
          Course,
          AssignmentDocument,
          PostAssignment,
          PostTutorial,
          Content,
          Unit
          )
from Applications.Administration.models import (
          Standard
          )    

from Applications.Examination.models import (
        CourseResult,
        FinalResult
        )          
          

from django.views.generic import (
           CreateView,
           DeleteView,
           DetailView,
           UpdateView,
           ListView,
           TemplateView,
           )
           
from django.core.cache import cache

from django.contrib import messages

import datetime

from Applications.Education.forms import (
         PostAssignmentForm,
         PostTutorialForm
         )

from Applications.Core.loader import CacheLoader



class AllCoursesView(ListView,CacheLoader):
    model = Course
    template_name = 'AllCoursesPage.html'
    context_object_name = 'courses'
    
    def get_context_data(self,**kwargs):
        kwargs=self.load_cache(kwargs)
        kwargs = self.load_cache(kwargs)
        return super().get_context_data(**kwargs)

class StandardCoursesListView(DetailView,CacheLoader):
    model = Standard
    template_name = 'AllCoursesPage.html'
    context_object_name = 'courses'
    
    
    
    def get_context_data(self,**kwargs):
        kwargs['standards']=Standard.objects.all()
        kwargs['courses']=Course.objects.filter(standard=self.object)
        kwargs=self.load_cache(kwargs)
        return super().get_context_data(**kwargs) 


'''
------------------------------------
      STUDENT RELATED VIEWS...
'''
'''
  COURSES RELATED VIEWS....
'''
class CourseListView(ListView,CacheLoader):
	model = Course
	context_object_name='courses'
	template_name = 'CourseListPage.html'
	def get_queryset(self,**kwargs):
	    queryset = []
	    for course_result in FinalResult.objects.get(student=cache.get('channel')).courses_result.all():
	        queryset.append(course_result.course)
	    return queryset
	def get_context_data(self,**kwargs):
	    kwargs['result']=FinalResult.objects.get(student=cache.get('channel'))
	    kwargs['student']=cache.get('channel')
	    kwargs=self.load_cache(kwargs)
	    return super().get_context_data(**kwargs)
    
    
class CourseDetailView(DetailView,CacheLoader):
	model = Course
	context_object_name = 'course'
	
	def get_template_names(self):
	    channel = cache.get('channel')
	    if channel.is_staff:
	        return 'StaffBlogPage.html'
	    elif channel.is_manager:
	        return 'ManagerBlogPage.html'
	    else:
	        return 'ProfileLayerPage.html'
	
	def is_registered(self,student):
		try:
		    CourseResult.objects.get(student=student,course=self.object)
		    return True
		except:
		    return False
		   
	
	def get_context_data(self,**kwargs):
	    kwargs['student']=cache.get('channel')
	    kwargs=self.load_cache(kwargs)
	    
	    kwargs['courses']=Course.objects.filter(standard=self.object.standard)
	    
	    kwargs['has_logged_in']=True
	    kwargs['standards']=Standard.objects.all()
	    kwargs['is_registered']=self.is_registered(cache.get('channel'))
	    kwargs['main_template']='CourseDetailPage.html'
	    kwargs['side_template']='AllCoursesSideBarPage.html'
	    #kwargs['content']=self.get_content()
	    return super().get_context_data(**kwargs)
	    
	def get_content(self,**kwargs):
	    try:
	        return Content.objects.get(course='Python')
	    except:
	        return Content.objects.create(course=self.object.course_name)
	     
	    
	        
	        
	    	
	
	
class ExCourseDetailView(DetailView,CacheLoader):
    model = Course
    template_name = 'CourseDetailPage.html'
    context_object_name = 'course'	    


class RegisterCourseView(DetailView,CacheLoader):
    model = Course
    context_object_name = 'course'
    
    def get_template_names(self):
    	if self.get_course_result():
    		return 'CourseRegisterOnSuccessPage.html'
    	else:
    		return 'CourseRegisterOnFailurePage.html'
            
    
    def get_context_data(self,**kwargs):
        try:
            kwargs['student']=cache.get('channel')
            kwargs=self.load_cache(kwargs)
            return super().get_context_data(**kwargs)
        
        except:
            return redirect('Main:LoginPage')
        
    def get_course_result(self):
        student = cache.get('channel')
        course = CourseResult(
        course=self.object)
        credentials = {
        'student':student,
        'internal marks':0,
        'external marks':0,
        'total marks':0,
        'percentage':0,
        'grade':'NA',
        'passed':False,
        'course':self.object,
        }
        return course.register(credentials)	   	   
	
def SearchCourseView(request):
    try:
        course=Course.objects.get(course_name=request.GET['course'])
        return redirect('Education:CourseDetailPage',pk=course.pk)
    except:
        messages.add_message(request,20,'OOPS.....NO COURSE FOUND')
        return redirect('Education:AllCoursesPage')


'''
------------------------------------
  COURSE CONTENT RELATED VIEWS...
'''
class UnitPDFView(DetailView,CacheLoader):
	model = Unit
	template_name = 'PDFViewPage.html'
	context_object_name = 'unit'
	
	
	
	def get_context_data(self,**kwargs):
	    contents=cache.get('contents')
	    kwargs['contents']=contents
	    
	    
	    index = 0
	    for content in contents:
	        index += 1
	        if self.object.code==content.code:
	            break
	    try:
	        kwargs['next']=contents[index+1]
	    except:
	        kwargs['next']=False
	    try:
	        kwargs['previous']=contents[index-1]
	    except:
	        kwargs['previous']=False
	    kwargs['content']=cache.get('content')
	    kwargs['student']=cache.get('channel')
	    kwargs=self.load_cache(kwargs)
	    return super().get_context_data(**kwargs)
	    
#url content/1/	    
class ContentPDFView(DetailView,CacheLoader):
	model = Content
	template_name = 'PDFViewPage.html'
	def get_context_data(self,**kwargs):
	    contents = self.object.units.all()
	    cache.set('contents',contents)
	    cache.set('content',self.object)
	    kwargs['content']=self.object
	    kwargs['contents']=contents
	    kwargs['unit']=contents[0]
	    
	    try:
	        kwargs['next']=contents[1]
	    except:
	        kwargs['next']=False
	    try:
	        kwargs['previous']=contents[-1]
	    except:
	        kwargs['previous']=False
	    kwargs['student']=cache.get('channel')
	    kwargs=self.load_cache(kwargs)
	    return super().get_context_data(**kwargs)
		
		
class DownloadUnitPDFView(DetailView,CacheLoader):
    model = Unit
    template_name = 'UnitPDFPage.html'
    context_object_name = 'unit'
    
    def get_context_data(self,**kwargs):
	    kwargs['student']=cache.get('channel')
	    kwargs=self.load_cache(kwargs)
	    return super().get_context_data(**kwargs)






'''
------------------------------------
  STUDENT  ASSIGNMENT RELATED VIEWS
'''


class AssignmentListView(ListView,CacheLoader):
	template_name='BlogPage.html'
	context_object_name='assignments'
	
	def get_queryset(self,**kwargs):
		return AssignmentDocument.objects.filter(uploaded_by=cache.get('channel'),is_drafted=False)
		
	def get_context_data(self,**kwargs):
	    kwargs['student']=cache.get('channel')
	    kwargs=self.load_cache(kwargs)
	    kwargs['drafts']=False
	    kwargs['main_template']='AssignmentListPage.html'
	    kwargs['side_template']='CoursesSideBarPage.html'
	    return super().get_context_data(**kwargs)


class SubmittedAssignmentsListView(ListView,CacheLoader):
	template_name='BlogPage.html'
	context_object_name='assignments'
	
	def get_queryset(self,**kwargs):
		return AssignmentDocument.objects.filter(uploaded_by=cache.get('channel'),is_drafted=False,is_submitted=True)
		
	def get_context_data(self,**kwargs):
	    kwargs['student']=cache.get('channel')
	    kwargs=self.load_cache(kwargs)
	    kwargs['drafts']=False
	    kwargs['main_template']='AssignmentListPage.html'

	    kwargs['side_template']='CoursesSideBarPage.html'
	    return super().get_context_data(**kwargs)

	  
#url assignments/all/
class PendingAssignmentsListView(ListView,CacheLoader):
	template_name='BlogPage.html'
	context_object_name='assignments'
	
	def get_queryset(self,**kwargs):
		return AssignmentDocument.objects.filter(uploaded_by=cache.get('channel'),is_drafted=False,is_submitted=False)
		
	def get_context_data(self,**kwargs):
	    kwargs['student']=cache.get('channel')
	    kwargs=self.load_cache(kwargs)
	    kwargs['drafts']=False
	    kwargs['main_template']='AssignmentListPage.html'

	    kwargs['side_template']='CoursesSideBarPage.html'
	    return super().get_context_data(**kwargs)			
def CourseAssignmentsListView(request,course_name):
    assignments = AssignmentDocument.objects.filter(uploaded_by=cache.get('channel').username,course_name=course_name)
    channel = cache.get('channel')
    context = {
    'assignments':assignments,
    'channel':channel,
    'title':'COURSE CONTENT',
    'student':channel,
    'drafts':False,
    'main_template':'AssignmentListPage.html',
    'side_template':'CoursesSideBarPage.html'
    }
    return render(request,'BlogPage.html',context)
    
	
class AssignmentDetailView(DetailView,CacheLoader):
	model = AssignmentDocument
	template_name='BlogPage.html'
	context_object_name = 'assignmentdocument'
	
	def get_context_data(self,**kwargs):
		cache.set('assignment',self.object)
		kwargs['is_open']=self.object.is_open()
		kwargs['assignment']=PostAssignment.objects.get(code=self.object.code)
		kwargs['student']=cache.get('channel')
		kwargs=self.load_cache(kwargs)
		kwargs['main_template']='AssignmentDetailPage.html'
		kwargs['side_template']='CoursesSideBarPage.html'
		return super().get_context_data(**kwargs)

#url assignment/submit/
def submit_assignment(request):
	document = request.GET['document']
	assignment = cache.get('assignment')
	assignment.submit(document)
	if assignment.flag:
	     messages.add_message(request,20,'Assignment Successfully Submitted')
	     return redirect('Education:AssignmentListPage')
	else:
	    messages.add_message(request,20,'NO FILE SELECTED')
	    return redirect('Education:AssignmentDetailPage',pk=assignment.pk)	    
	
class UpdateAssignmentView(UpdateView):
    model = AssignmentDocument
    fields = ['document']
    template_name = 'BlogPage.html'
    context_object_name = 'assignment'
    
    def form_valid(self,form,**kwargs):
        if self.request.GET['document'] is not None:
            return super().form_valid(form)
        else:
            messages.add_message(request,20,'NO DOCUMENT')
            return redirect('Education:EditAssignmentPage',self.object.pk)
    
    def get_context_data(self,**kwargs):
        cache.set('assignment',self.object)
        kwargs['student']=cache.get('channel')
        kwargs=self.load_cache(kwargs)
        kwargs['main_template']='EditAssignmentPage.html'
        kwargs['side_template']='CoursesSideBarPage.html'
        return super().get_context_data(**kwargs)
        

def AddAssignmentToDraftView(request,pk):
    assignment = AssignmentDocument.objects.get(pk=pk)
    assignment.is_drafted=True
    assignment.save()
    messages.add_message(request,20,'Successfully Added To Draft')
    return redirect('Education:AssignmentListPage')
    
def RemoveAssignmentFromDraftView(request,pk):
    assignment = AssignmentDocument.objects.get(pk=pk)
    assignment.is_drafted=False
    assignment.save()
    messages.add_message(request,20,'Successfully Removed From Draft')
    return redirect('Education:AssignmentListPage')
    
class DraftedAssignmentsView(ListView,CacheLoader):
    model = AssignmentDocument
    template_name='BlogPage.html'
    context_object_name='assignments'
    
    def get_queryset(self,**kwargs):
        return AssignmentDocument.objects.filter(uploaded_by=cache.get('channel').username,is_drafted=True)
        
    def get_context_data(self,**kwargs):
        kwargs['student']=cache.get('channel')
        kwargs=self.load_cache(kwargs)
        kwargs['drafts']=True
        kwargs['main_template']='AssignmentListPage.html'
        kwargs['side_template']='CoursesSideBarPage.html'
        return super().get_context_data(**kwargs) 

        

'''
-----------------------------------
   STAFF RELATED VIEWS.....
'''

''' 
----------------------------------
        COURSES RELATED...
'''
class StaffCoursesListView(ListView,CacheLoader):
    model =Course
    template_name = 'StaffBlogPage.html'
    context_object_name='courses'
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='StaffCourseListPage.html'
        kwargs=self.load_cache(kwargs)
        return super().get_context_data(**kwargs)
    	
    
    def get_queryset(self):
        return cache.get('channelcontent').courses.all()
        

class StaffCourseDetailView(DetailView,CacheLoader):
    model=Course
    template_name = 'StaffBlogPage.html'
    context_object_name = 'course'
    
    def get_context_data(self,**kwargs):
        cache.set('course',self.object)
        kwargs['main_template']='StaffCourseDetailPage.html'
        kwargs=self.load_cache(kwargs)
        try:
            kwargs['content_obj']=Content.objects.get(course_name=self.object.course_name)
            kwargs['content']=True
        except:
            kwargs['content']=False
        return super().get_context_data(**kwargs)
        
''' 
----------------------------------
        ASSIGNMENTS RELATED...
'''        
class PostAssignmentCreateView(TemplateView,CacheLoader):
    template_name = 'StaffBlogPage.html'
    
    def get_context_data(self,**kwargs):
        kwargs['course']=cache.get('course')
        code=str(cache.get('course').course_code)+str(len(PostAssignment.objects.filter(course=cache.get('course'))))
        kwargs['code']=code
        kwargs=self.load_cache(kwargs)
        kwargs['main_template']='PostAssignmentCreatePage.html'
        kwargs=self.load_cache(kwargs)
        return super().get_context_data(**kwargs)
        
    def post(self,request):
        channel=cache.get('channel')
        assignment=PostAssignment(
        question=request.POST['question'],
        title=request.POST['title'],
        message=request.POST['message'],
        due_date=request.POST['date'],
        course=cache.get('course'))
        if True:
            assignment.save()
            return redirect('Education:PostedAssignmentDetailPage',pk=assignment.pk)
        else:
            messages.add_message(request,20,'OOPS SOMETHING WENT WRONG')
            return redirect('Education:PostAssignmentCreatePage')



class PostedAssignmentListView(DetailView,CacheLoader):
    model=Course
    template_name = 'StaffBlogPage.html' 
    context_object_name = 'course'
    
    def get_context_data(self,**kwargs):
        channelcontent = cache.get('channelcontent')
        kwargs['assignments']=channelcontent.get_assignments_of(self.object)
        kwargs['main_template']='StaffCoursePostedAssignmentListPage.html'
        kwargs=self.load_cache(kwargs)
        return super().get_context_data(**kwargs)        


    
    
        
class StaffSubmittedAssignmentListView(DetailView,CacheLoader):
    model = PostAssignment
    template_name = 'StaffBlogPage.html'
    context_object_name = 'post_assignment'
    
    def get_context_data(self,**kwargs):
        kwargs['assignments']=self.object.submissions.all()
        kwargs['main_template']='SubmittedAssignmentListPage.html'
        kwargs=self.load_cache(kwargs)
        return super().get_context_data(**kwargs)
        

class PostedAssignmentDetailView(DetailView,CacheLoader):
    model = PostAssignment
    template_name = 'StaffBlogPage.html'
    context_object_name = 'assignment'
    
    def get_context_data(self,**kwargs):
        channelcontent = cache.get('channelcontent')
        kwargs['main_template']='PostedAssignmentDetailPage.html'
        kwargs=self.load_cache(kwargs)
        return super().get_context_data(**kwargs)
    

def PostedAssignmentDeleteView(request,pk):
    PostAssignment.objects.get(pk=pk).delete()
    messages.add_message(request,20,'deleted successfully')
    return redirect('Education:StaffPostedAssignmentListPage',pk=cache.get('course').pk)
        
    
        

    
    
    
    
    
        
class PostedTestListView(ListView,CacheLoader):
    model=Course
    template_name = 'StaffCourseDetailPage.html'
    
    def get_context_data(self,**kwargs):
        channelcontent = cache.get('channelcontent')
        kwargs['assignments']=[]
        kwargs['tests']=channelcontent.get_tests_of(self.object)
        
        
        
        return super().get_context_data(**kwargs)




'''
------------------------------------
    TUTORAILS RELATED VIEWS....
'''

class StaffPostTutorialCreateView(TemplateView,CacheLoader):
    template_name = 'StaffBlogPage.html'
    
    def get_context_data(self,**kwargs):
        kwargs['course']=cache.get('course')
        channelcontent = cache.get('channelcontent')
        kwargs['main_template']='StaffPostTutorialCreatePage.html'
        kwargs=self.load_cache(kwargs)
        return super().get_context_data(**kwargs)
        
        
    def post(self,request):
        title = request.POST['title']
        description = request.POST['description']
        information = request.POST['document']
        PostTutorial(
        course=cache.get('course'),
        title=title,
        description=description,
        information=information).save()
        return redirect('Education:StaffPostedTutorialListPage',pk=cache.get('course').pk)



class StaffPostedTutorialListView(DetailView,CacheLoader):
    model = Course
    template_name = 'StaffBlogPage.html'
    context_object_name = 'course'
    
    def get_context_data(self,**kwargs):
        kwargs['tutorials']=PostTutorial.objects.filter(course=self.object)
        cache.set('course',self.object)
        channelcontent = cache.get('channelcontent')
        kwargs['main_template']='StaffPostTutorialListPage.html'
        kwargs=self.load_cache(kwargs)
        return super().get_context_data(**kwargs)
        


        
        
class StaffPostedTutorialDetailView(DetailView,CacheLoader):
    model = PostTutorial
    template_name = 'StaffPostTutorialDetailPage.html'
    context_object_name = 'tutorial'
    

def StaffPostedTutorialDeleteView(request,pk):
	PostTutorial.objects.get(pk=pk).delete()
	messages.add_message(request,30,'POSTED TUTORIAL DELETED SUCCESSFULLY')
	return redirect('Education:StaffPostedTutorialListPage')

class StaffCourseContentDetailView(DetailView,CacheLoader):
	model = Content
	template_name = 'StaffBlogPage.html'
	context_object_name = 'content'
	
	def get_context_data(self,**kwargs):
		kwargs['course']=cache.get('course')
		channelcontent = cache.get('channelcontent')
		kwargs['main_template']='StaffCourseContentDetailPage.html'
		kwargs=self.load_cache(kwargs)
		cache.set('course_content',self.object)
		return super().get_context_data(**kwargs)
		
		
class StaffAddUnitToContentView(TemplateView,CacheLoader):
	template_name = 'StaffAddUnitToCourseContentPage.html'
	
	def get_context_data(self,**kwargs):
			kwargs['main_template']='StaffCourseContentDetailPage.html'
			kwargs = self.load_cache(kwargs)
			
			kwargs=self.load_cache(kwargs)
			return super().get_context_data(**kwargs)
		
	def post(self,request):
		unit = Unit(
		this_content = cache.get('course_content'),
		code=request.POST['code'],
		title=request.POST['title'],
		introduction = request.POST['introduction'],
		information = request.POST['information'],
		practice_questions = request.POST['pratice_questions'],
		summary = request.POST['summary'],
		)
		unit.save()
		course_content = cache.get('course_content')
		course_content.references +='#' +unit.code
		course_content.save()
		messages.add_message(request,20,'UNIT ADDED SUCCESSFULY')
		return redirect('Education:StaffCourseContentDetailPage',pk=unit.this_content.pk)
		
	

def StaffRemoveUnitFormContentView(request,pk):
	Unit.objects.get(pk=pk).delete()
	messages.add_message(request,20,'UNIT REMOVED SUCCESSFULLY')
	return redirect('Education:StaffCourseContentDetailPage',pk=cache.get('course_content').pk)



def StaffCourseContentCreateView(request,pk):
    course = Course.objects.get(pk=pk)
    content = Content(
    course=course)
    content.save()
    return redirect('Education:StaffCourseContentDetailPage',pk=content.pk)
    
