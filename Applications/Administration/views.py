#Importing required modules for the administration system
#template rendering
from django.shortcuts import (render,redirect)

from Applications.Administration.models import (
                Channel,
                TCForm,
                Standard,
                ChangeMobileNumberForm,
                FeedBack,
                Appointment,
                Department,
                AdmissionForm
                )

from Applications.Administration.forms import (
               ApplicationForm,
               TCFormClass,
              
               )
from Applications.Main.models import (ChannelContent,StaffChannelContent)

from Applications.Education.models import (Course,Content,Unit)

from Applications.DashBoard.models import Circular

from Applications.Management.models import (Event,Management)


from Applications.DashBoard.models import (Circular)

from Applications.Transactions.models import FeeReminder

from Applications.Core.loader import CacheLoader




from django.views.generic import (TemplateView,ListView,DetailView,DeleteView)

from django.core.cache import cache
from django.views.generic import (
TemplateView,DetailView)
from django.views.generic.edit import (
         CreateView,
         ModelFormMixin,
         FormView,
         
           )
from django.views.generic.edit import FormMixin

from mysite.siteconf import (
CASTES,LANGUAGES,STANDARDS,PAYMENT_FORMS
)

from django.contrib import messages 

from datetime import datetime   
from django.core.cache import cache




 
#returns code for the model 
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
#-----------------------------------

			
#Find outs application using
#registration number
#http:127.0.0.1:8000/applications/<int:pk>/status/

class ApplicationStatusView(DetailView,CacheLoader):
    model = AdmissionForm
    template_name = 'HomePage.html'
    context_object_name ='application'
    
    def get_context_data(self,**kwargs):
        kwargs['template']='ApplicationStatusPage.html'
        if self.object.status=='ADMITTED':
            cache.set('admission_document',self.object)
            kwargs['has_process_url']=True
        return super().get_context_data(**kwargs)
		

#searches the application using the
#registration number
#http:127.0.0.1:8000/applications/search/
class SearchApplicationView(TemplateView,CacheLoader):
    template_name = 'HomePage.html'
    
    def get_context_data(self,**kwargs):
        kwargs['template']='ApplicationSearchPage.html'
        return super().get_context_data(**kwargs)
        
    def post(self,request):
        registration_number = request.POST['reg_number']
        try:
            application = AdmissionForm.objects.get(reg_number=registration_number)
            return redirect('Admin:ApplicationStatusPage',pk=application.pk)
        except:
            messages.add_message(request,20,'NO APPLICATION FOUND ON REGISTERED NUMBER.....')
            return redirect('Admin:ApplicationSearchPage') 

#Deletes the application
#http:127.0.0.1:8000/applications/<int:pk>/delete/
def ApplicationDeleteView(request,pk):
	AdmissionForm.objects.get(pk=pk).delete()
	messages.add_message(request,30,'ADMISSION FORM DELETED SUCCESSFULLY')
	return redirect('Admin:AdmissionListPage')
	
#----------------------------------
#Application Status Page
#http:127.0.0.1:8000/tc/apply/	    
class ApplyTCView(TemplateView,CacheLoader):
    def get_template_names(self):
        channel = cache.get('channel')
        if channel.is_staff:
            return 'StaffBlogPage.html'
        elif channel.is_manager:
            return 'ManagerBlogPage.html'
        else:
            return 'ProfileLayerPage.html'
    
    def get_context_data(self,**kwargs):
	    kwargs=self.load_cache(kwargs)
	    kwargs['date']=datetime.today()
	    kwargs['main_template']='ApplyTCPage.html'
	    return super().get_context_data(**kwargs)
	    
    def post(self,request):
        reason=request.POST['reason']
        tc = TCForm.objects.get_or_create(channel=cache.get('channel'),
	    status='APPLIED',
	    fee_section=False,
	    granted=False)[0]
        tc.reason = reason
        tc.save()
        messages.add_message(request,20,'YOUR APPLICATION WILL BE SENT FOR AUTHORISATION.......')
        return redirect('Admin:ProfilePage',pk=cache.get('channel').pk)



#http:127.0.0.1:8000/<int:pk>/profile/
class ProfilePageView(DetailView,CacheLoader):
    model = Channel
    template_name = 'ProfileLayerPage.html'
    context_object_name = 'channel'
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='ProfilePage.html'
        kwargs['header_template']='IndexBar.html'
        try:
            kwargs['channel']=cache.get('channel')
            kwargs['student']=cache.get('channel')
        except:
            kwargs['channel']=Channel.objects.get(pk=self.args[0])
            kwargs['channelcontent']=self.object.get_channel_content()
        return super().get_context_data(**kwargs)
        
        

        
#----------------------------------
#Change MobileNumberS
#http:127.0.0.1:8000/profile/mobile_number/change
     
class ChangeMobileNumberView(TemplateView,CacheLoader):
    
    
    def get_template_names(self):
        channel = cache.get('channel')
        if channel.is_staff:
            return 'StaffBlogPage.html'
        elif channel.is_manager:
            return 'ManagerBlogPage.html'
        else:
            return 'ProfileLayerPage.html'
            
    def get_context_data(self,**kwargs):
        
        kwargs=self.load_cache(kwargs)
        kwargs['main_template']='ChangeMobileNumberPage.html'
        return super().get_context_data(**kwargs)
        
    def post(self,request):
        new_number = request.POST['number']
        reason = request.POST['reason']
        channel = cache.get('channel')
        changenumber = ChangeMobileNumberForm.objects.get_or_create(
        channel=channel,
            is_verified=False
            )[0]
        changenumber.reason=reason
        changenumber.new_number = new_number
        changenumber.save()
        messages.add_message(request,20,'MOBILE NUMBER WILL RESET SOON')
        if channel.is_staff:
            return redirect('Education:StaffCoursesListPage')
        return redirect('Admin:ProfilePage',pk=channel.pk)
        
        
#Gives FeedBack of the user
#http:127.0.0.1:8000/profile/feedback/ 
class FeedBackView(TemplateView,CacheLoader):
    def get_template_names(self):
        channel = cache.get('channel')
        if channel.is_staff:
            return 'StaffBlogPage.html'
        elif channel.is_manager:
            return 'ManagerBlogPage.html'
        else:
            return 'ProfileLayerPage.html'
            
    def get_context_data(self,**kwargs):
        
        kwargs=self.load_cache(kwargs)
        
        kwargs['main_template']='FeedBackPage.html'
        return super().get_context_data(**kwargs)
        
    def post(self,request):
        feedback_text = request.POST['text']
        channel = cache.get('channel')
        feedback_obj = FeedBack.objects.get_or_create(
        channel=channel
        )[0]
        feedback_obj.feedback = feedback_text
        feedback_obj.save()
        messages.add_message(request,20,'THANKS FOR YOUR FEEDBACK')
        if channel.is_staff:
            return redirect('Education:StaffCoursesListPage')
        else:
            return redirect('Admin:ProfilePage',pk=channel.pk)
        
        
#Access to the Appointment of page
#http:127.0.0.1:8000/profile/appointment/       
class AppointmentFormView(TemplateView,CacheLoader):
    def get_template_names(self):
        channel = cache.get('channel')
        if channel.is_staff:
            return 'StaffBlogPage.html'
        elif channel.is_manager:
            return 'ManagerBlogPage.html'
        else:
            return 'ProfileLayerPage.html'
            
    def get_context_data(self,**kwargs):
        kwargs=self.load_cache(kwargs)
        kwargs['main_template']='AppointmentFormPage.html'
        return super().get_context_data(**kwargs)
        
    def post(self,request):
        meeting_reason = request.POST['reason']
        meeting_session = request.POST['session'] 
        channel = cache.get('channel')
        meeting_obj = Appointment.objects.get_or_create(
        channel=channel
        )[0]
        meeting_obj.session=meeting_session
        meeting_obj.reason = meeting_reason
        meeting_obj.on_date = request.POST["date"]
        print(request.POST['date'])
        meeting_obj.save()
        messages.add_message(request,20,'YOUR APPOINMENT WILL BE AUTHORISED SOON...')
        return redirect('Admin:ProfilePage',pk=cache.get('channel').pk)
        

#Manager >  Adminstartion Employee
#http:127.0.0.1:8000/manager/detail/
#http:127.0.0.1:8000/manager/
#Managers are used to add course
#ManagerBlogPage.....
#all the related manager views

#http:127.0.0.1:8000/manager/


class ManagerBlogView(TemplateView,CacheLoader):
    template_name = 'ManagerBlogPage.html'
    
    def get_context_data(self,**kwargs):
        
        kwargs['main_template']='ManagerIndexBlogPage.html'
        kwargs['departments']=Department.objects.all()
        kwargs=self.load_cache(kwargs)


        return super().get_context_data(**kwargs)



'''
-----------------------------------
      MANAGER COURSE VIEWS
      
http:127.0.0.1:8000/manager/course/
create/
'''
class ManagerCourseCreateView(TemplateView,CacheLoader):
    template_name = 'ManagerBlogPage.html'
    
    def get_context_data(self,**kwargs):
        kwargs['standards']=Standard.objects.all()
        kwargs['main_template']='CourseCreatePage.html'
        kwargs['staffs']=Channel.objects.filter(is_staff=True)
        kwargs = self.load_cache(kwargs)       
        return super().get_context_data(**kwargs)
        
    def post(self,request):
        
        new_course = Course(
        course_name = request.POST['course_name'],
        course_code = request.POST['course_code'],
        standard = Standard.objects.get(pk=request.POST['standard']),
        incharge = Channel.objects.get(username=request.POST['incharge']),
        outcomes = request.POST['outcomes']
        )
        
        try:
            new_course.save()
            return redirect('Admin:ManagerCourseDetailPage',pk=new_course.pk)
        except:
            messages.add_message(request,30,'OOPS SOMETHING WENT WRONG')
            return redirect('Admin:ManagerCourseListPage')
            
'''
http:127.0.0.1:8000/manager/course/
all/
'''         
class ManagerCourseListView(ListView,CacheLoader):
    model = Course
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'courses'
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='DepartmentListPage.html'
        kwargs['courses_page']=True
        kwargs = self.load_cache(kwargs)   
        return super().get_context_data(**kwargs)            
       
'''
http:127.0.0.1:8000/manager/course/
<int:pk>/details/
'''        
class ManagerCourseDetailView(DetailView,CacheLoader):
   model = Course
   template_name = 'ManagerBlogPage.html'
   context_object_name = 'course'
   
   def get_context_data(self,**kwargs):
       kwargs['main_template']='CourseDetailPage.html'
       kwargs = self.load_cache(kwargs)
       kwargs['context_manager'] =True
       return super().get_context_data(**kwargs)
       
       
'''
http:127.0.0.1:8000/manager/course/
<int:pk>/delete/
'''
def ManagerCourseDeleteView(request,pk):
    Course.objects.get(pk=pk).delete()
    messages.add_message(request,30,'COURSE SUCCESSFULLY DELETED')
    return redirect('Admin:ManagerCourseListPage')
    

       
'''
-----------------------------------
     MANAGER STANDARD VIEWS

http:127.0.0.1:8000/manager/standard
/create/
'''

class ManagerStandardCreateView(TemplateView,CacheLoader):
    template_name = 'ManagerBlogPage.html'
    
    def get_context_data(self,**kwargs):
        kwargs['staffs']=Channel.objects.filter(is_staff=True)
        kwargs['main_template']='StandardCreatePage.html'
        kwargs = self.load_cache(kwargs)   
        return super().get_context_data(**kwargs)
        
    def post(self,request):
        standard= int(request.POST['standard'])
        incharge = Channel.objects.get(pk =int(request.POST['incharge']))
        '''
        ***
        TRYING TO GET STANDARD
        ***
        '''
        try:
            new_standard = Standard.objects.get_or_create(
        standard=standard)[0]
        except:
            new_standard = Standard.objects.get_or_create(
        standard=standard)
        new_standard.incharge = incharge
        '''
        ***
        TRYING TO ADD STANDARD
        ***
        '''
        try:
            new_standard.save()
            messages.add_message(request,40,'SUCCESSFULLY ADDED STANDARD.....')
            return redirect('Admin:ManagerStandardDetailPage',pk=new_standard.pk)
        except:
            messages.add_message(request,40,'OOPS!....SOMETHING WENT WRONG')
            return redirect('Admin:ManagerStandardListPage')
        
       
'''
http:127.0.0.1:8000/manager/standard
/all/
'''
class StandardListView(ListView,CacheLoader):
    model = Standard
    template_name = 'DepartmentListPage.html'
    context_object_name = 'standards'
    
    
    def get_context_data(self,**kwargs):
        kwargs['standards_page']=True
        kwargs = self.load_cache(kwargs)   
        return super().get_context_data(**kwargs)
        

'''
http:127.0.0.1:8000/manager/standard
/<int:pk>/details/
'''      
class ManagerStandardListView(ListView,CacheLoader):
    model = Standard
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'standards'
    
    def plot_animations(self):
        from Applications.Core.animation import FitModel
        animation = FitModel()
        animation.fix_queryset(Standard.objects.all())
        animation.get_standard_rows()
        animation.get_standard_values()
        animation.set_labels(x_label='Standard',
        y_label='Strength',
        title='Standard Strength')
        animation.set_bar()
        animation.save_as_image()
       
    def plot_pie_animations(self):
        from Applications.Core.animation import FitModel       
        animation1 = FitModel()
        animation1.fix_queryset(Standard.objects.all())
        animation1.get_standard_rows()
        animation1.get_standard_values()
        animation1.set_pie()
        
    def setup(self,request,*args,**kwargs):
        if True:
            self.plot_animations()
            self.plot_pie_animations()
        return super().setup(request,*args,**kwargs)
        
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='DepartmentListPage.html'
        kwargs['standards_page']=True
        kwargs = self.load_cache(kwargs)   
        kwargs['image']='icons/standardanimation.png'
        return super().get_context_data(**kwargs)
        
       
    def dispatch(self,request,*args,**kwargs):
        self.REVERSE = True
        return super().dispatch(request,*args,**kwargs)
            
   
        
       
'''
http:127.0.0.1:8000/manager/standard
/<int:pk>/details/
'''        
class ManagerStandardDetailView(DetailView,CacheLoader):
    model = Standard
    template_name = 'ManagerBlogPage.html'
    context_object_name='standard'
    
    def get_context_data(self,**kwargs):
        kwargs['standard_courses']=Course.objects.filter(standard=self.object)
        kwargs = self.load_cache(kwargs)   
        kwargs['main_template']='StandardDetailPage.html'
        return super().get_context_data(**kwargs)

      
'''
http:127.0.0.1:8000/manager/standard
/<int:pk>/delete/
'''    
def ManagerStandardDeleteView(request,pk):
    Standard.objects.get(pk=pk).delete()
    messages.add_message(request,30,'STANDARD SUCCESSFULLY DELETED')
    return redirect('Admin:ManagerStandardListPage')
    





'''
     MANAGER ADMISSION VIEWS
http:127.0.0.1:8000/manager/standard
/<int:pk>/details/
'''      

#Admission form view
#creates admission form
#http:127.0.0.1:8000/admissions/
#apply/

class AdmissionFormView(TemplateView,CacheLoader):
	template_name = 'HomePage.html'
	
	def get_context_data(self,**kwargs):
	    kwargs['template']='StudentApplicationForm.html'
	      
	    return super().get_context_data(**kwargs)
	
	
	def post(self,request,**kwargs):
	    admission_form = AdmissionForm()
	    admission_form.fullname = request.POST['fullname']
	    admission_form.mobile_number = request.POST['mobile']
	    admission_form.father_name = request.POST['fathername']
	    admission_form.email_id = request.POST['mail']
	    admission_form.standard = request.POST['standard']
	    admission_form.reg_number ='AP'+'2020'+'ST'+str(request.POST['standard'])+str(request.POST['fullname'][0:2]).upper()
	    try:
	        admission_form.save()
	        messages.add_message(request,20,'YOUR APPLICATION WILL BE FURTHER PROCESSEDED....')
	        from Applications.Core.Connector import connector
	        from Applications.Core.mailing_context import ADMISSION_APPROVE_MAIL
	        connector.server()
	        connector.connect(admission_form.email_id)
	        connector.mailformat(
	        ADMISSION_APPROVE_MAIL['Subject'],
	        ADMISSION_APPROVE_MAIL['Body'].format(admission_form.reg_number),
	        ADMISSION_APPROVE_MAIL['Image'],
	        ADMISSION_APPROVE_MAIL['Document']
	        )
	        connector.sendmail()
	        return redirect('Admin:ApplicationStatusPage',pk=admission_form.pk)
	    except:
	        messages.add_message(request,20,'OOPS..!! COULD NOT PROCESS APPLICATION....')
	        return redirect('Main:HomePage')



'''
http:127.0.0.1:8000/manager/
admissions/all/
'''      
class ManagerAdmissionListView(ListView,CacheLoader):
    model = AdmissionForm
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'admissions'
    
    
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='DepartmentListPage.html'
        kwargs['admissions_page']=True
        kwargs = self.load_cache(kwargs) 
        kwargs['title']='ADMISSIONS'
        return super().get_context_data(**kwargs)
        
'''
http:127.0.0.1:8000/manager/
admissions/<int:pk/details/
'''            
class AdmissionDetailView(DetailView,CacheLoader):
    model = AdmissionForm
    template_name = 'AdmissionStatusPage.html'
    context_object_name = 'application'
    
    def get_context_data(self,**kwargs):
        
        kwargs['title']='ADMISSIONS'
        return super().get_context_data(**kwargs)  
        
'''
http:127.0.0.1:8000/manager/
admissions/<int:pk/details/
'''          
class ManagerAdmissionDetailView(DetailView,CacheLoader):
    model = AdmissionForm
    template_name = 'ManagerBlogPage.html'
    context_object_name ='application'
    
    def get_context_data(self,**kwargs):
       kwargs['main_template']='ApplicationStatusPage.html'
       kwargs['has_redirect_url']=True
       
       if self.object.status=='ADMITTED':
           
           kwargs['redirect_url']='Admin:ManagerDiscardAdmissionPage'
           kwargs['button_text']='DISCARD-ADMISSION'
           
       else:
           
           kwargs['redirect_url']='Admin:ManagerApproveAdmissionPage'
           kwargs['button_text']='APPROVE-ADMISSION'
       kwargs = self.load_cache(kwargs) 
       return super().get_context_data(**kwargs)
       
'''
http:127.0.0.1:8000/manager/
admissions/<int:pk/approve/
'''         
def ManagerApproveAdmissionView(request,pk):
    application = AdmissionForm.objects.get(pk=pk)
    application.status ='ADMITTED'
    application.save()
    messages.add_message(request,20,'APPLICATION APPROVED SUCCESSFULLY..........')
    return redirect('Admin:ManagerAdmissionListPage')

class ManagerAdmissionDeleteView(DeleteView):
    model = AdmissionForm
    
    def get_success_url(self):
        return redirect('Admin:ManagerAdmissionListPage')
'''
http:127.0.0.1:8000/manager/
admissions/<int:pk/discard/
'''    
def ManagerDiscardAdmissionView(request,pk):
    application = AdmissionForm.objects.get(pk=pk)
    application.status ='REJECTED'
    application.save()
    messages.add_message(request,20,'APPLICATION REJECTED SUCCESSFULLY.......')
    return redirect('Admin:ManagerAdmissionListPage')
    
    

class ManagerApproveAdmissionListView(ListView,CacheLoader):
    model = AdmissionForm
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'admissions'
    
    def get_queryset(self):
        return AdmissionForm.objects.filter(approved=True)
    
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='DepartmentListPage.html'
        kwargs['admissions_page']=True
        kwargs = self.load_cache(kwargs) 
        kwargs['title']='APPROVED ADMISSIONS'
        return super().get_context_data(**kwargs)
        
                
                        
class ManagerDiscardAdmissionListView(ListView,CacheLoader):
    model = AdmissionForm
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'admissions'
    
    def get_queryset(self):
        return AdmissionForm.objects.filter(approved=False)
    
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='DepartmentListPage.html'
        kwargs['admissions_page']=True
        kwargs = self.load_cache(kwargs) 
        kwargs['title']='DISCARDED ADMISSIONS'
        return super().get_context_data(**kwargs)                                 
        
'''
------------------------------------
     MANAGER STAFF RELATED VIEWS
http:127.0.0.1:8000/manager/
admissions/all/
'''    
        
        
        
        
'''
http:127.0.0.1:8000/manager/staffs
/create/
'''
class ManagerStaffCreateView(TemplateView,CacheLoader):
	template_name = 'ManagerBlogPage.html'
	
	def get_context_data(self,**kwargs):
	    kwargs['castes']=CASTES
	    kwargs['languages']=LANGUAGES
	    kwargs['main_template']='ChannelCreatePage.html'
	    kwargs = self.load_cache(kwargs) 
	    kwargs['standards']=STANDARDS
	    return super().get_context_data(**kwargs)
	    
	def post(self,request):
	    standard = Standard.objects.get_or_create(standard=int(request.POST['standard']))[0]
	    channel = Channel(
	    username=request.POST['username'],
	    father_name=request.POST['fathername'],
	    mother_name=request.POST['mothername'],
	    caste = request.POST['caste'],
	    email=request.POST['email'],
	    mobile_number=request.POST['mobile'],
	    language = request.POST['language'],
	    profile = request.POST['profile'],
	    section='A',
	    is_staff=True,
	    status='STUDENT',
	    standard=standard,
	    rollnumber=0,
	    admission_number =0,
	    key='key'
	    )
	    try:
	        channel.save()
	        messages.add_message(request,20,f'{channel.username} added successfully')
	        return redirect('Admin:ManagerStaffListPage')
	    except:
	        messages.add_message(request,40,'OOPS...SOMETHING WENT WRONG....\nCAN NOT ADD STAFF')
	        return redirect('Admin:ManagerStaffListPage')                    
'''
http:127.0.0.1:8000/manager/staffs
/all/
'''              
class ManagerStaffListView(ListView,CacheLoader):
    model = Channel
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'channels'
    
    def get_queryset(self):
        return self.model.objects.filter(is_staff=True)
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='DepartmentListPage.html'
        kwargs['staffs_page']=True
        kwargs['channel']=cache.get('channel')
        kwargs['channelcontent']=cache.get('channelcontent')
        return super().get_context_data(**kwargs)
        
'''
http:127.0.0.1:8000/manager/staffs
/<int:pk>/details/
'''  
class ManagerStaffDetailView(DetailView,CacheLoader):
	model = Channel
	template_name = 'ManagerBlogPage.html'
	context_object_name = 'thischannel'
	
	def get_context_data(self,**kwargs):
	    kwargs['main_template']='ManagerProfilePage.html'
	    kwargs = self.load_cache(kwargs) 
	    return super().get_context_data(**kwargs)
		
		
'''
http:127.0.0.1:8000/manager/staffs
/<int:pk>/details/
'''  
class ManagerStaffEditView(DetailView,CacheLoader):
	model = Channel
	template_name = 'StaffIndexPage.html'
	context_object_name = 'channel'
	
	def get_context_data(self,**kwargs):
	    kwargs = self.load_cache(kwargs) 
	    return super().get_context_data(**kwargs)


class StaffProfileView(DetailView,CacheLoader):
	model = StaffChannelContent
	template_name = 'StaffBlogPage.html'
	context_object_name = 'channel'
	
	def get_context_data(self,**kwargs):
		kwargs = self.load_cache(kwargs) 
		kwargs['main_template']='ProfilePage.html'
		return super().get_context_data(**kwargs)
				
'''
------------------------------------
  MANAGER STUDENT PAGE.....
http:127.0.0.1:8000/manager/staffs
/create/
'''
class ManagerChannelCreateView(TemplateView,CacheLoader):
	template_name = 'HomePage.html'
	
	def get_context_data(self,**kwargs):
	    kwargs['template']='ChannelCreatePage.html'
	    kwargs['castes']=CASTES
	    kwargs['languages']=LANGUAGES
	    kwargs = self.load_cache(kwargs)  
	    kwargs['standards']=STANDARDS
	    return super().get_context_data(**kwargs)
	    
	def post(self,request):
	    channel = Channel(
	    username=request.POST['username'],
	    father_name=request.POST['fathername'],
	    mother_name=request.POST['mothername'],
	    caste = request.POST['caste'],
	    email=request.POST['email'],
	    mobile_number=request.POST['mobile'],
	    language = request.POST['language'],
	    profile = request.POST['profile'],
	    section='A',
	    is_staff=False,
	    status='STUDENT',
	    standard=Standard.objects.get(standard=request.POST['standard']),
	    rollnumber=0,
	    admission_number =0,
	    key='key'
	    )
	    try:
	        messages.add_message(request,20,f"Channel Added Successfully")
	        channel.save()
	        return redirect("Main:LoginPage")
	    except:
	        messages.add_message(request,20,"Oops Something went wrong.....")
	        return redirect("Main:HomePage")
	        
	        
	    	    
'''
http:127.0.0.1:8000/manager/staffs
/<int:pk>/delete/
'''          
def ManagerStaffDeleteView(request,pk):
    Channel.objects.get(pk=pk).delete()
    messages.add_message(request,20,'CHANNEL SUCCESSFULLY DELETED...')
    return redirect('Admin:ManagerStaffListPage')
	
class ManagerChannelListView(ListView,CacheLoader):
    model = Channel
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'channels'
    
    def get_queryset(self):
        return self.model.objects.filter(is_staff=False)
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='DepartmentListPage.html'
        kwargs['channels_page']=True
        kwargs = self.load_cache(kwargs) 
        return super().get_context_data(**kwargs)		
		            

'''
------------------------------------
    MANAGER EVENTS RELATED VIEWS
http:127.0.0.1:8000/manager/
eventas/create/
'''        
class ManagerEventCreateView(TemplateView,CacheLoader):
	template_name = 'ManagerBlogPage.html'
	
	def get_context_data(self,**kwargs):
		kwargs['main_template']='EventCreatePage.html'
		kwargs['managements']=Management.objects.all()
		kwargs = self.load_cache(kwargs) 
		return super().get_context_data(**kwargs)
		
	def post(self,request):
	    try:
	        poster = request.POST['poster']
	    except:
	        poster=None
	    event = Event(
	    event=request.POST['event'],
	    vision=request.POST['vision'],
	    image=poster,
	    management=Management.objects.get(pk=request.POST['management']),
	    date=request.POST['date']
	    )
	    event.save()
	    return redirect('Admin:ManagerEventListPage')    


'''
http:127.0.0.1:8000/manager/
events/all/
'''    
class ManagerEventListView(ListView,CacheLoader):
    model = Event
    template_name = 'ManagerBlogPage.html'
    context_object_name='events'
    
    def get_context_data(self,**kwargs):
       kwargs['main_template']='DepartmentListPage.html'
       kwargs['events_page']=True
       kwargs = self.load_cache(kwargs) 
       return super().get_context_data(**kwargs)
       
'''
http:127.0.0.1:8000/manager/
events/<int:pk>/details/
'''
class ManagerEventDetailView(DetailView,CacheLoader):
    model = Event
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'event'
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='EventDetailPage.html'
        kwargs['context_manager']=True
        kwargs = self.load_cache(kwargs) 
        kwargs['manager_event_details']=True
        return super().get_context_data(**kwargs)


'''
http:127.0.0.1:8000/manager/
events/<int:pk>/delete/
'''
def ManagerEventDeleteView(request,pk):
	Event.objects.get(pk=pk).delete()
	messages.add_message(request,20,'EVENT DELETED SUCCESSFULLY')
	return redirect('Admin:ManagerEventListPage')

   

   
'''
------------------------------------
    MANAGER RELATED CIRCULARS VIEWS
http:127.0.0.1:8000/manager/
circulars/create/
'''                       
class ManagerCircularCreateView(TemplateView,CacheLoader):
	template_name = 'ManagerBlogPage.html'
	
	def get_context_data(self,**kwargs):
		kwargs['main_template']='ContextCreatePage.html'
		kwargs['title']='CIRCULAR'
		kwargs['departments_page']=True	
		kwargs['departments']=Department.objects.all()
		kwargs = self.load_cache(kwargs) 
		return super().get_context_data(**kwargs)
		
	def post(self,request):
	    title = request.POST['title']
	    message = request.POST['message']
	    sender=Department.objects.get(pk=request.POST['department'])
	    code='CR'+str(get_chunk_code(title))+str(Circular.objects.count())+str(get_chunk_code(title))
	    circular = Circular(
        code=code,
        sender=sender,
        title=title,
        message=message,
        )
	    circular.save()
	    return redirect('Admin:ManagerCircularListPage')       


'''
http:127.0.0.1:8000/manager/
circulars/all/
'''                
class ManagerCircularListView(ListView,CacheLoader):
    model = Circular
    template_name = 'ManagerBlogPage.html'
    context_object_name='circulars'
    
    def get_context_data(self,**kwargs):
       kwargs['main_template']='DepartmentListPage.html'
       kwargs['circulars_page']=True
       kwargs = self.load_cache(kwargs) 
       return super().get_context_data(**kwargs)
       

'''
http:127.0.0.1:8000/manager/
circulars/<int:pk/details/
'''   
class ManagerCircularDetailView(DetailView,CacheLoader):
    model = Circular
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'context'
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='ContextDetailPage.html'
        kwargs['context_manager']=True
        kwargs = self.load_cache(kwargs) 
        return super().get_context_data(**kwargs)



'''
http:127.0.0.1:8000/manager/
circulars/<int:pk/delete/
'''   
def ManagerCircularDeleteView(request,pk):
	Circular.objects.get(pk=pk).delete()
	messages.add_message(request,20,'CIRCULAR DELETED SUCCESSFULLY')
	return redirect('Admin:ManagerCircularListPage')





		
		

		

		

        
'''
------------------------------------
    MANAGER MANAGEMENT RELATED VIEWS
http:127.0.0.1:8000/manager/
managements/create/
'''  

class ManagerManagementCreateView(TemplateView,CacheLoader):
    template_name = 'ManagerBlogPage.html'
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='ManagementCreatePage.html'
        kwargs['staffs']=Channel.objects.filter(is_staff=True)
        kwargs = self.load_cache(kwargs) 
        return super().get_context_data(**kwargs)
        
    def post(self,request):
        management = Management(
        name = request.POST['name'],
        head=Channel.objects.get(pk=request.POST['head']),
        )
        try:
            management.save()
            messages.add_message(request,20,'MANAGEMENT ADDED SUCCESSFULLY')
        except:
            messages.add_message(request,20,'UNABLE TO CREATE MANAGEMENT....')
        try:
            co_ordinators = Channel.objects.filter(pk=request.POST['coordinators'])
            for coordinator in co_ordinators:
                management.co_ordinaters.add(coordinator)
        except:
            messages.add_message(request,20,'NO CO ORDINATORS ADDED...')
        return redirect('Admin:ManagerManagementListPage')
        
'''
http:127.0.0.1:8000/manager/
managements/all/
'''  
class ManagerManagementListView(ListView,CacheLoader):
    model = Management
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'managements'
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='DepartmentListPage.html'
        kwargs['managements_page']=True
        kwargs = self.load_cache(kwargs) 
        return super().get_context_data(**kwargs)

'''
http:127.0.0.1:8000/manager/
managements/<int:pk>/details/
'''  
class ManagerManagementDetailView(DetailView,CacheLoader):
    model = Management
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'management'
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='ManagerCommiteeDetailPage.html'
        kwargs['management_page']=True
        kwargs = self.load_cache(kwargs) 
        return super().get_context_data(**kwargs)





'''
http:127.0.0.1:8000/manager/
managements/<int:pk>/delete/
'''  
def ManagerManagementDeleteView(request,pk):
	Management.objects.get(pk=pk).delete()
	messages.add_message(request,30,'Management Deleted Successfully')
	return redirect('Admin:ManagerManagementListPage')
	
'''
http:127.0.0.1:8000/manager/
managements/<int:pk>/details/
'''  
class ManagerManagementChangeHeadView(DetailView,CacheLoader):
    model = Management
    template_name = 'ManagerMemberShipPage.html'
    context_object_name='object'
    
    def get_context_data(self,**kwargs):
        kwargs = self.load_cache(kwargs) 
        kwargs['staffs']=Channel.objects.all()
        kwargs['redirect_url']='Admin:ManagerManagementChangeHeadView'
        return super().get_context_data(**kwargs)
        
    def change_head(request,pk):
        management=Management.objects.get(pk=pk)
        my_object = Channel.objects.get(pk=request.POST['newobject'])
        management.head=my_object
        management.save()
        messages.add_message(request,30,f'{my_object.username} appointed as head successfully........')
        return redirect('Admin:ManagerManagementDetailPage',pk=management.pk)

class ManagerManagementAddMemberView(DetailView,CacheLoader):
    model = Management
    template_name = 'ManagerMemberShipPage.html'
    context_object_name='object'
    
    def get_context_data(self,**kwargs):
        kwargs = self.load_cache(kwargs) 
        kwargs['staffs']=Channel.objects.all()
        kwargs['redirect_url']='Admin:ManagerManagementAddMemberView'
        return super().get_context_data(**kwargs)
                
                        
    def add_member(request,pk):
        management=Management.objects.get(pk=pk)
        my_object = Channel.objects.get(pk=request.POST['newobject'])
        management.co_ordinaters.add(my_object)
        messages.add_message(request,30,f'{my_object.username} added successfully........')
        return redirect('Admin:ManagerManagementDetailPage',pk=management.pk)
         
        
def ManagerManagementRemoveMemberView(request,management,pk):
    management=Management.objects.get(pk=management)
    my_object = Channel.objects.get(pk=pk)
    management.co_ordinaters.remove(my_object)
    messages.add_message(request,30,f'{my_object.username} removed successfully........')
    return redirect('Admin:ManagerManagementDetailPage',pk=management.pk)



'''
------------------------------------
    MANAGER MANAGEMENT RELATED VIEWS
http:127.0.0.1:8000/manager/
departments/create/
'''  
class ManagerDepartmentCreateView(TemplateView,CacheLoader):
    template_name = 'ManagerBlogPage.html'
    
    def get_context_data(self,**kwargs):
        
        kwargs['staffs']=Channel.objects.filter(is_staff=True)
        kwargs = self.load_cache(kwargs)  
        kwargs['main_template']='DepartmentCreatePage.html'
        
        return super().get_context_data(**kwargs)
        
    def post(self,request):
        department = Department(
        title=request.POST['name'],
        head=Channel.objects.get(pk=request.POST['head']),
        vision=request.POST['vision'],
        message=request.POST['message'],
        )
        try:
            department.save()
            messages.add_message(request,20,'DEPARTMENT ADDED SUCCESSFULLY')
        except:
            messages.add_message(request,20,'UNABLE TO CREATE DEPARTMENT....')
        try:
            members = Channel.objects.filter(pk=request.POST['members'])
            for member in members:
                department.members.add(member)
        except:
            messages.add_message(request,20,'DEPARTMENT CREATED SUCCESSFULLY\nNO MEMBERS ADDED')
        return redirect('Admin:ManagerDepartmentListPage')

'''
http:127.0.0.1:8000/manager/
departments/<int:pk>/details/
'''  
class ManagerDepartmentListView(ListView,CacheLoader):
    model = Department
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'departments'
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='DepartmentListPage.html'
        kwargs['members']=Channel.objects.filter(is_staff=True)
        kwargs = self.load_cache(kwargs) 
        return super().get_context_data(**kwargs)
        
    def post(self,request):
        pass


'''
http:127.0.0.1:8000/manager/
departments/<int:pk>/details/
'''  
class ManagerDepartmentDetailView(DetailView,CacheLoader):
    model = Department
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'department'
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='ManagerCommiteeDetailPage.html'
        kwargs = self.load_cache(kwargs) 
        return super().get_context_data(**kwargs)


'''
http:127.0.0.1:8000/manager/
departments/<int:pk>/details/
'''  
class ManagerDepartmentEditView(DetailView,CacheLoader):
    model = Department
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'managements'
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='DepartmentListPage.html'
        kwargs['managements_page']=True
        kwargs = self.load_cache(kwargs) 
        return super().get_context_data(**kwargs)



'''
http:127.0.0.1:8000/manager/
managements/<int:pk>/details/
'''  
class ManagerDepartmentChangeHeadView(DetailView,CacheLoader):
    model = Department
    template_name = 'ManagerMemberShipPage.html'
    context_object_name='object'
    
    def get_context_data(self,**kwargs):
        kwargs = self.load_cache(kwargs) 
        kwargs['staffs']=Channel.objects.all()
        kwargs['redirect_url']='Admin:ManagerDepartmentChangeHeadView'
        return super().get_context_data(**kwargs)
        
    def change_head(request,pk):
        department=Department.objects.get(pk=pk)
        my_object = Channel.objects.get(pk=request.POST['newobject'])
        department.head=my_object
        department.save()
        messages.add_message(request,30,f'{my_object.username} appointed as head successfully........')
        return redirect('Admin:ManagerDepartmentDetailPage',pk=department.pk)

class ManagerDepartmentAddMemberView(DetailView,CacheLoader):
    model = Department
    template_name = 'ManagerMemberShipPage.html'
    context_object_name='object'
    
    def get_context_data(self,**kwargs):
        kwargs = self.load_cache(kwargs) 
        kwargs['staffs']=Channel.objects.all()
        kwargs['redirect_url']='Admin:ManagerDepartmentAddMemberView'
        return super().get_context_data(**kwargs)
                
                        
    def add_member(request,pk):
        department=Department.objects.get(pk=pk)
        my_object = Channel.objects.get(pk=request.POST['newobject'])
        department.members.add(my_object)
        messages.add_message(request,30,f'{my_object.username} added successfully........')
        return redirect('Admin:ManagerDepartmentDetailPage',pk=department.pk)
         
        
def ManagerDepartmentRemoveMemberView(request,department,pk):
    department=Department.objects.get(pk=department)
    my_object = Channel.objects.get(pk=pk)
    department.members.remove(my_object)
    messages.add_message(request,30,f'{my_object.username} removed successfully........')
    return redirect('Admin:ManagerDepartmentDetailPage',pk=department.pk)



















'''
http:127.0.0.1:8000/manager/
departments/<int:pk>/delete/
'''  
def ManagerDepartmentDeleteView(request,pk):
	Department.objects.get(pk=pk).delete()
	messages.add_message(request,30,'Department Deleted Successfully')
	return redirect('Admin:ManagerDepartmentListPage')






        
class StandardDetailView(DetailView,CacheLoader):
    model = Standard
    template_name = 'StandardDetailPage.html'
    context_object_name='standard'
    
    def get_context_data(self,**kwargs):
        kwargs['standard_courses']=Course.objects.filter(standard=self.object)
        return super().get_context_data(**kwargs)



def ManagerPostFeeReminderView(request,pk):
    fr = FeeReminder.objects.get(pk=pk)
    from Applications.Core.feereminder import FeeReminderSystem
    frs = FeeReminderSystem(fr.month)
    frs.send_messages()
    messages.add_message(request,20,"MESSAGES SENT THE PENDING STUDENTS")
    return redirect('Admin:ManagerFeeReminderListPage')



class ManagerFeeReminderListView(ListView,CacheLoader):
    model = FeeReminder
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'months'
	
    def get_context_data(self,**kwargs):
        kwargs['fee_reminders_page']=True
        kwargs['main_template']='DepartmentListPage.html'
        kwargs = self.load_cache(kwargs) 
        return super().get_context_data(**kwargs)
		
		

        
		
class ManagerChangeNumberListView(ListView,CacheLoader):
    model = ChangeMobileNumberForm
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'applications'
    
    
    def get_context_data(self,**kwargs):
        kwargs['change_mobilenumbers_page']=True
        kwargs['main_template']='DepartmentListPage.html'
        kwargs = self.load_cache(kwargs) 
        return super().get_context_data(**kwargs)        


class ManagerResultAnimationView(DetailView,CacheLoader):
    model = Department
    template_name = 'ManagerResultAnimationPage.html'
    context_object_name = 'object'
    
    def setup(self,request,*args,**kwargs):
        from Applications.Core.animation import FitModel
        animation = FitModel()
        animation.install_sheet()
        animation.get_marks_sheet_as_df()
        animation.fit_passed_students_model()
        animation.set_labels(x_label='Courses',y_label='Results',title='Students Results')
        animation.save_as_image()
        return super().setup(request,*args,**kwargs)
        
    def get_context_data(self,*args,**kwargs):
        kwargs = self.load_cache(kwargs) 
        return super().get_context_data(**kwargs)




class ManagerTCFormDetailView(DetailView,CacheLoader):
	model = TCForm
	template_name = 'ManagerBlogPage.html'
	context_object_name = 'application'
	
	def get_context_data(self,**kwargs):
		kwargs = self.load_cache(kwargs) 	
		kwargs['main_template']='ManagerTCFormDetailPage.html'
		
		return super().get_context_data(**kwargs)
		

class ManagerTCFormListView(ListView,CacheLoader):
    model = TCForm
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'applications'
    
    def get_context_data(self,**kwargs):
        kwargs['TC_applications_page']=True
        kwargs['main_template']='DepartmentListPage.html'
        kwargs = self.load_cache(kwargs) 
        kwargs['title']='ALL APPLICATIONS'
        return super().get_context_data(**kwargs)


def ManagerTCFormApproveView(request,pk):
	application = TCForm.objects.get(pk=pk)
	application.granted = True
	application.save()
	messages.add_message(request,20,"TRANSFER CERTIFICATE RECIEVED SUCCESSFULLY....")
	return redirect('Admin:ManagerTCFormListPage')


def ManagerTCFormDiscardView(request,pk):
	application = TCForm.objects.get(pk=pk)
	application.granted = False
	application.save()
	messages.add_message(request,20,"SORRY CAN NOT DELETE...")
	return redirect('Admin:ManagerTCFormListPage')
	

def ManagerTCFormDeleteView(request,pk):
	TCForm.objects.get(pk=pk).delete()
	messages.add_message(request,20,"Successfully deleted the form")
	return redirect('Admin:ManagerTCFormListPage')


class ManagerTCFormApproveListView(ListView,CacheLoader):
    model = TCForm
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'applications'
    
    def get_queryset(self):
        return TCForm.objects.filter(granted=True)
        
    def get_context_data(self,**kwargs):
    	kwargs = self.load_cache(kwargs) 	
    	kwargs['main_template']='DepartmentListPage.html'
    	kwargs['TC_applications_page']=True
    	kwargs['title']='APPROVED APPLICATIONS'
    	return super().get_context_data(**kwargs)
    	
class ManagerTCFormDiscardListView(ListView,CacheLoader):
    model = TCForm
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'applications'
    
    def get_queryset(self):
        return TCForm.objects.filter(granted=False)
        
    def get_context_data(self,**kwargs):
    	kwargs = self.load_cache(kwargs) 	
    	kwargs['main_template']='DepartmentListPage.html'
    	kwargs['TC_applications_page']=True
    	kwargs['title']='DISCARD APPLICATIONS'
    	return super().get_context_data(**kwargs)

class ManagerApproveAppointmentListView(ListView,CacheLoader):
	model = Appointment
	template_name = 'ManagerAppointmentSchedulePage.html'
	context_object_name = 'appointments'
	
	def get_queryset(self):
		return Appointment.objects.filter(success=True)
	
	def get_context_data(self,**kwargs):
		kwargs=self.load_cache(kwargs)
		return super().get_context_data(**kwargs)
		
		
		
def ManagerAppointmentDeleteView(request,pk):
	appointment = Appointment.objects.get(pk=pk)
	appointment.delete()
	messages.add_message(request,20,"Appointment Deleted Successfully")
	return redirect('Admin:ManagerTCFormListPage')
		




class ManagerAppointmentListView(ListView,CacheLoader):
	model = Appointment
	template_name = 'ManagerBlogPage.html'
	context_object_name = 'appointments'
	
	def get_context_data(self,**kwargs):
		kwargs=self.load_cache(kwargs)
		kwargs['main_template']='DepartmentListPage.html'
		kwargs['appointments_page']=True
		kwargs['title']='APPOINTMENTS'
		return super().get_context_data(**kwargs)
		
		
class ManagerAppointmentDetailView(DetailView,CacheLoader):
	model = Appointment
	template_name = 'ManagerBlogPage.html'
	context_object_name = 'appointment'
	
	def get_context_data(self,**kwargs):
		kwargs['channel']=cache.get("channel")
		kwargs['channelcontent'] = cache.get("channelcontent")
		kwargs['main_template']='ManagerAppointmentDetailPage.html'
		return super().get_context_data(**kwargs)
		

def ManagerAppointmentApproveView(request,pk):
	appointment = Appointment.objects.get(pk=pk)
	appointment.success = True
	appointment.save()
	messages.add_message(request,20,'Appointment Approved Sucessfuly')
	return redirect("Admin:ManagerAppointmentListPage")
	
def ManagerAppointmentDiscardView(request,pk):
	appointment = Appointment.objects.get(pk=pk)
	appointment.success = False
	appointment.save()
	messages.add_message(request,20,'Appointment discarded Sucessfuly')
	return redirect("Admin:ManagerAppointmentListPage")
	
class ManagerApproveAppointmentListView(ListView,CacheLoader):
	model = Appointment
	template_name = 'ManagerBlogPage.html'
	context_object_name = 'appointments'
	
	def get_queryset(self):
		return Appointment.objects.filter(success=True)
	
	def get_context_data(self,**kwargs):
		kwargs=self.load_cache(kwargs)
		kwargs['main_template']='DepartmentListPage.html'
		kwargs['appointments_page']=True
		kwargs['title']='APPROVED APPOINTMENTS'
		return super().get_context_data(**kwargs)
		


class ManagerDiscardAppointmentListView(ListView,CacheLoader):
	model = Appointment
	template_name = 'ManagerBlogPage.html'
	context_object_name = 'appointments'
	
	def gey_queryset(self):
		return Appointment.objects.filter(success=False)

	def get_context_data(self,**kwargs):
		kwargs=self.load_cache(kwargs)
		kwargs['main_template']='DepartmentListPage.html'
		kwargs['appointments_page']=True
		kwargs['title']='DISCARD APPOINTMENTS'
		return super().get_context_data(**kwargs)
		
		
def ManagerAppointmentDeleteView(request,pk):
	appointment = Appointment.objects.get(pk=pk)
	appointment.delete()
	messages.add_message(request,20,"Appointment Deleted Successfully")
	return redirect('Admin:ManagerTCFormListPage')
		

class ManagerFeedBackListView(ListView,CacheLoader):
    model = FeedBack
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'feedbacks'
    
    def get_context_data(self,**kwargs):
        kwargs=self.load_cache(kwargs)
        
        kwargs['main_template']='ManagerFeedBackListPage.html'
        
        return super().get_context_data(**kwargs)
    
    
    
    
class ManagerDraftedFeedBackListView(ListView,CacheLoader):
    model = FeedBack
    template_name = 'ManagerBlogPage.html'
    context_object_name = 'feedbacks'
    
    def get_queryset(self):
        return FeedBack.objects.filter(is_drafted=True)
        
    def get_context_data(self,**kwargs):
        kwargs=self.load_cache(kwargs)
        
        kwargs['drafts']=True
        kwargs['main_template']='ManagerFeedBackListPage.html'
        
        return super().get_context_data(**kwargs)
    

  
class ManagerFeedBackReplyView(TemplateView,CacheLoader):
	model = FeedBack
	template_name = 'FeedBackPage.html'
	context_object_name = 'feedback'
	
	def get_context_data(self,**kwargs):
	    kwargs=self.load_cache(kwargs)
	    return super().get_context_data(**kwargs)
        
#    def post(self,request,pk):
#    	feedback_text = request.POST['text']
#    	feed_back = FeedBack.objects.get(pk=pk)
#    	feed_back.reply_text = feedback_text
#    	feed_back.save()
#    	messages.add_message(request,20,'REPLIED TO FEEDBACK')
#    	return redirect('Admin:ManagerFeedBackListPage')
        
        
def ManagerAddFeedBackToDraftView(request,pk):
    feedback = FeedBack.objects.get(pk=pk)
    feedback.is_drafted = True
    feedback.save()
    messages.add_message(request,20,'ADDED TO DRAFT')
    return redirect('Admin:ManagerFeedBackListPage')




def ManagerRemoveFeedBackFromDraftView(request,pk):
    feedback = FeedBack.objects.get(pk=pk)
    feedback.is_drafted = False
    feedback.save()
    messages.add_message(request,20,'REMOVED FROM DRAFT')
    return redirect('Admin:ManagerFeedBackListPage')
    
def ManagerFeedBackDeleteView(request,pk):
   feedback = FeedBack.objects.get(pk=pk)
   feedback.delete()
   messages.add_message(request,20,'DELETED SUCCESSFULLY')
   return redirect('Admin:ManagerFeedBackListPage')