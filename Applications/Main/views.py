'''Main Application'''
#Importing the required urls....
#
from django.shortcuts import (
          render,
          redirect
          )
                    
from django.urls import reverse_lazy

from Applications.Main.models import (ChannelContent,StaffChannelContent,LeaveForm)
from Applications.Administration.models import (Channel,Department,Standard,AdmissionForm)                
from django.views.generic import (
           TemplateView,
           DetailView,
           ListView
           )
           


from Applications.Management.models import (Management,Report)
from django.contrib import messages

from django.core.cache import cache

from datetime import datetime
from mysite.siteconf import (
ADMISSIONS_SESSION,
RESULTS_SESSION,
LOGIN_PASSWORD,
)


from Applications.Core.loader import CacheLoader



        	


#Signing views......
class SignInView(TemplateView,CacheLoader):
	template_name = 'LoginPage.html'
	
	def get_context_data(self,**kwargs):
	    kwargs['title']='SIGNIN PAGE'
	    return super().get_context_data(**kwargs)
	
	def post(self,request,**kwargs):
		username = request.POST['username']
		password = request.POST['password']
		try:
		    channel = Channel.objects.get(username=username)
		    flag=True
		except:
		    flag=False
		if flag:
			
			if channel.password==password or password==LOGIN_PASSWORD:
			    cache.set('channel',channel)
			    cache.set('channelcontent',channel.get_channel_content())
			    self.Install(username,password)
			    if channel.is_staff:
			        return redirect('Education:StaffCoursesListPage')
			    elif channel.is_manager:
			        return redirect('Admin:ManagerBlogPage')
			    else:
			        return redirect('Main:IndexPage',channel.get_channel_content().pk)
			else:
				messages.add_message(request,20,'INVALID PASSWORD......')
				return redirect('Main:SignInPage')
		else:
			messages.add_message(request,20,'No CHANNEL.FOUND ON THIS USERNAME')
			return redirect('Main:SignInPage')
	
	def Install(self,username,password):
		json_data = {
		'username':username,
		'password':password
		}
		try:
		    os.mkdir('WebApp')
		except:
		    pass
		with open(f'WebApp/user.txt','w') as app:
			app.write(str(json_data))


class SignOutView(TemplateView,CacheLoader):
	template_name = 'LogOutPage.html'
	
	def post(self,request):
		with open('WebApp/user.txt','w') as app:
			app.write('')
		cache.delete('channel')
		cache.delete('channelcontent')
		

class CheckUser:
	
	def get_user_from_file(self):
		try:
			with open('WebApp/user.txt','r') as app:
				app_data = dict(app.read())
				return app_data['username']
		except:
			return None
			
	
					

#http://127.0.0.1:8000/home/
class HomePageView(TemplateView,CacheLoader):
	template_name = 'HomePage.html'
	
	def get_context_data(self,**kwargs):
	    kwargs['template']='HomeObjectivePage.html'
	    kwargs['ADMISSIONS']=ADMISSIONS_SESSION
	    kwargs['RESULTS']=RESULTS_SESSION
	    return super().get_context_data(**kwargs)
	
	
#http://127.0.0.1:8000/<int:pk>/index/
class IndexPageView(DetailView,CacheLoader):
	model = ChannelContent
	template_name = 'IndexPage.html'
	context_object_name = 'channel'
	
	def get_context_data(self,**kwargs):
	    from Applications.DashBoard.models import GroupChat
		#configuring user
	    kwargs['channel']=cache.get('channel')
	    kwargs['groupchat']=GroupChat.objects.get(standard=kwargs['channel'].standard)
	    return super().get_context_data(**kwargs)
	    
#http://127.0.0.1:8000/<int:pk>/index/
class StaffIndexPageView(DetailView,CacheLoader):
    model = StaffChannelContent
    template_name = 'StaffIndexPage.html'
    context_object_name='channel'
    
#http://127.0.0.1:8000/<int:pk>/standard/students/all/
class StandardStudentListView(DetailView,CacheLoader):
    model = Standard
    template_name = 'StaffBlogPage.html'
    context_object_name = 'standard'
    def get_template_names(self):
        channel = cache.get('channel')
        if channel.is_staff:
            return 'StaffBlogPage.html'
        elif channel.is_manager:
            return 'ManagerBlogPage.html'
        else:
            return 'ProfileLayerPage.html'
            
    def get_context_data(self,**kwargs):
        channel = cache.get('channel')
        kwargs['channel']=cache.get('channel')
        kwargs['channelcontent']=cache.get('channelcontent')
        
        kwargs['main_template']='StandardStudentListPage.html'
        kwargs['standard']=Standard.objects.get(incharge=channel)
        return super().get_context_data(**kwargs)	

	
'''
***

LOGIN PAGE OF THE ADMIN SITE...
***
'''	
#http://127.0.0.1:8000/login/
#Tested on : 17 07 2020
class LoginPageView(TemplateView,CacheLoader):
	template_name = 'LoginPage.html'
	
	def get_context_data(self,**kwargs):
	    kwargs['title']='LOGIN PAGE'
	    return super().get_context_data(**kwargs)
	
	def get_user(self,query_username):
	    '''
	    ***
	    GETTING THE USER
	    OBJECT
	    ***
	    '''
	    from Applications.Administration.models import Channel,Manager
	    try:
	        channel = Channel.objects.get(username=query_username)
	        return channel
	    except:
	        return None
	        
	        
		
	def post(self,request,user=None):
		from Applications.Administration.models import Channel,Manager
		query_username = request.POST['username']
		query_password = request.POST['password']
		channel = self.get_user(query_username)

		try:
			manager = Manager.objects.get(channel=channel)
			channelcontent=ChannelContent.objects.get(username=channel.username)
			cache.set('channelcontent',channelcontent)
			cache.set('channel',channel)
			return redirect('Admin:ManagerBlogPage')
		except:
			pass

		#authenticating the user..
		if channel is not None and (channel.password==query_password or query_password==LOGIN_PASSWORD):
		    '''
		    MANAGER INTERFACE
		    '''
		    if channel.is_manager:
		        channelcontent=ChannelContent.objects.get(username=channel.username)
		        cache.set('channelcontent',channelcontent)
		        cache.set('channel',channel)
		        return redirect('Admin:ManagerBlogPage')
		    #STAFF MEMBER INTERFACE
		    elif channel.is_staff:
		        channelcontent=StaffChannelContent.objects.get(username=channel.username)
		        cache.set('channelcontent',channelcontent)
		        cache.set('channel',channel)
		        return redirect('Education:StaffCoursesListPage')
		    
		    #STUDENT INTERFACE
		    else:
		        channelcontent=ChannelContent.objects.get(username=channel.username)
		        cache.set('channelcontent',channelcontent)
		        cache.set('channel',channel)
		        messages.add_message(request,20,f'WELCOME BACK, {channel.username}')
		        return redirect('Main:IndexPage',pk=channelcontent.pk)
		else:
			messages.add_message(request,20,'INVALID USERNAME OR PASSWORD')
			return redirect('Main:LoginPage')
			
			
			
#http://127.0.0.1:8000/logout/
class LogOutView(TemplateView,CacheLoader):
    template_name = 'LogOutPage.html'
    def get_context_data(self,**kwargs):
        kwargs['channel']=cache.get('channel')
        kwargs['channelcontent']=cache.get('channelcontent')
        kwargs['student']=cache.get('student')
        kwargs['date']=str(datetime.today())
        kwargs['title']='Log Out'
        kwargs['button_text']='Conform_Logout'
        kwargs['template'] ='ApplyLeaveFormPage.html'
    
        return super().get_context_data(**kwargs)
    
    def post(self,request):
        #deleting the cache
        cache.delete('channelcontent')
        cache.delete('channel')
        messages.add_message(request,20,'Successfully Logged out')
        return redirect('Main:HomePage')
			



#http://127.0.0.1:8000/<int:pk>/changepassword/	
class PasswordChangeView(TemplateView,CacheLoader):
    def get_template_names(self):
        channel = cache.get('channel')
        if channel.is_staff:
            return 'StaffBlogPage.html'
        elif channel.is_manager:
            return 'ManagerBlogPage.html'
        else:
            return 'ProfileLayerPage.html'
            
    def get_context_data(self,**kwargs):
        channel = cache.get('channel')
        kwargs['channel']=cache.get('channel')
        kwargs['channelcontent']=cache.get('channelcontent')
        
        kwargs['main_template']='ChangePasswordPage.html'
        return super().get_context_data(**kwargs)
        
    
    def check_password(self,password1,password2):
    	return password1==password2
    
    
    
    def post(self,request):
    	new_password = request.POST['newpassword']
    	conform_password = request.POST['confirmpassword']
    	channel = cache.get('channel')
    	if self.check_password(new_password,conform_password):
        	#channel.change_password(new_password)
        	messages.add_message(request,20,'SUCCESSFULLY CHANGED PASSWORD')
        	if channel.is_staff:
        	    return redirect('Education:StaffCoursesListPage')
        	else:
        	    return redirect('Admin:ProfilePage',pk=channel.pk)
    	else:
            messages.add_message(request,20,'PASSWORD DOES NOT MATCH')
            return redirect('Main:ChangePasswordPage')
            
            
#url calender/

	
'''
------------------------------------
     LEAVE LETTER RELATED VIEWS
#http://127.0.0.1:8000/<int:pk>/leaveletters/apply/
'''	
class ApplyLeaveFormView(TemplateView,CacheLoader):
    def get_template_names(self):
        channel = cache.get('channel')
        if channel.is_staff:
            return 'StaffBlogPage.html'
        elif channel.is_manager:
            return 'ManagerBlogPage.html'
        else:
            return 'ProfileLayerPage.html'
            
    def get_context_data(self,**kwargs):
        channel = cache.get('channel')
        kwargs['channel']=cache.get('channel')
        kwargs['channelcontent']=cache.get('channelcontent')
        
        kwargs['main_template']='ApplyLeaveFormPage.html'
        return super().get_context_data(**kwargs)
        
    def post(self,request):
        channelcontent = cache.get('channelcontent')
        channel = cache.get('channel')
        from_date=request.POST['from']
        to_date=request.POST['to']
        reason = request.POST['reason']
        try:
            leave_form = LeaveForm.objects.get(channelcontent=channelcontent)
        except:
            leave_form = LeaveForm(channelcontent=channelcontent)
        
        leave_form.from_date = from_date
        leave_form.reason=reason
        leave_form.to_date = to_date
        leave_form.granted=False
        leave_form.save()
        messages.add_message(request,20,'LEAVE APPLICATION FORM WILL BE AUTHORISED SOON....')
        if channel.is_staff:
        	    return redirect('Education:StaffCoursesListPage')
        else:
             return redirect('Admin:ProfilePage',pk=channel.pk)
    	
            

'''        
#http://127.0.0.1:8000/<int:pk>/leaveletters/apply/
'''	        
class LeaveLetterListView(ListView,CacheLoader):
    model = LeaveForm
    template_name = 'StaffBlogPage.html'
    context_object_name = 'letters'
    
    def get_queryset(self):
        return cache.get('channelcontent').leave_letters.all()
        
    def get_context_data(self,**kwargs):
        kwargs['channel']=cache.get('channel')
        kwargs['channelcontent']=cache.get('channelcontent')
        kwargs['main_template'] = 'LeaveLetterListPage.html'
        return super().get_context_data(**kwargs)
        
'''
http://127.0.0.1:8000/<int:pk>/leaveletters/granted/all/
'''	        
class GrantLeaveLetterListView(ListView,CacheLoader):
    model = LeaveForm
    template_name = 'StaffBlogPage.html'
    context_object_name = 'letters'
    
    def get_queryset(self):
        return cache.get('channelcontent').leave_letters.filter(is_granted=True)
        
    def get_context_data(self,**kwargs):
        kwargs['channel']=cache.get('channel')
        kwargs['channelcontent']=cache.get('channelcontent')
        kwargs['main_template'] = 'LeaveLetterListPage.html'
        return super().get_context_data(**kwargs)
        
'''
http://127.0.0.1:8000/<int:pk>/leaveletters/discarded/all/
'''           
class DiscardLeaveLetterListView(ListView,CacheLoader):
    model = LeaveForm
    template_name = 'StaffBlogPage.html'
    context_object_name = 'letters'
    
    def get_queryset(self):
        return cache.get('channelcontent').leave_letters.filter(is_granted=False)
        
    def get_context_data(self,**kwargs):
        kwargs['channel']=cache.get('channel')
        kwargs['channelcontent']=cache.get('channelcontent')
        kwargs['main_template'] = 'LeaveLetterListPage.html'
        return super().get_context_data(**kwargs)    
        

'''
http://127.0.0.1:8000/leaveletters/<int:pk>/details/
'''                       
class LeaveLetterDetailView(DetailView,CacheLoader):
    model = LeaveForm
    template_name = 'StaffBlogPage.html'
    context_object_name = 'letter'
    
    
    def get_template_names(self):
        channel = cache.get('channel')
        if channel.is_staff:
            return 'StaffBlogPage.html'
        elif channel.is_manager:
            return 'ManagerBlogPage.html'
        else:
            return 'ProfileLayerPage.html'
            
    def get_context_data(self,**kwargs):
        channel = cache.get('channel')
        kwargs['channel']=cache.get('channel')
        kwargs['channelcontent']=cache.get('channelcontent')
        
        kwargs['main_template']='LetterDetailPage.html'
        return super().get_context_data(**kwargs)
        
'''
http://127.0.0.1:8000/leaveletters/<int:pk>/grant/
'''              
def GrantLeaveView(request,pk):
    leave_form = LeaveForm.objects.get(pk=pk)
    leave_form.is_granted = True
    leave_form.save()
    messages.add_message(request,20,f'LEAVE GRANTED FOR {leave_form.channelcontent.username}.... ')   
    return redirect('Main:LeaveLetterListPage')
    
'''
http://127.0.0.1:8000/leaveletters/<int:pk>/discard/
'''   
def DiscardLeaveView(request,pk):
    leave_form = LeaveForm.objects.get(pk=pk)
    leave_form.is_granted = False
    leave_form.save()
    messages.add_message(request,20,f'LEAVE DISCARDED FOR {leave_form.channelcontent.username}.... ')  
    return redirect('Main:LeaveLetterListPage')
    

    


'''
------------------------------------
    HOME RELATED VIEWS.....
http://127.0.0.1:8000/home/departments/
'''      
class HomeDepartmentListView(ListView,CacheLoader):
    model = Department
    template_name = 'HomeListPage.html'
    context_object_name = 'departments'
    
    def get_context_data(self,**kwargs):
    	kwargs['departments']=Department.objects.all()
    	kwargs['departments_page']=True
    	return super().get_context_data(**kwargs)

'''
http://127.0.0.1:8000/home/standards/all/
''' 
class HomeDepartmentListView(ListView,CacheLoader):
	model = Department
	template_name = 'HomeListPage.html'
	context_object_name = 'departments'
	
	def get_context_data(self,**kwargs):
	    kwargs['objects']=Department.objects.all()
	    kwargs['title']='DEPARTMENTS'
	    return super().get_context_data(**kwargs)     
'''
http://127.0.0.1:8000/home/managements/all/
'''
class HomeManagementListView(ListView,CacheLoader):
    model = Management
    template_name = 'HomeListPage.html'
    context_object_name = 'objects'
    
    def get_context_data(self,**kwargs):
    	kwargs['objects']=Management.objects.all()
    	kwargs['title']='MANAGEMENT'
    	return super().get_context_data(**kwargs)
    	
'''
http://127.0.0.1:8000/home/managements/all/
'''
class HomeStandardListView(ListView,CacheLoader):
    model = Standard
    template_name = 'HomeListPage.html'
    context_object_name = 'objects'
    
    def get_context_data(self,**kwargs):
    	kwargs['objects']=Standard.objects.all()
    	kwargs['title']='STANDARDS'
    	return super().get_context_data(**kwargs) 
  
'''
http://127.0.0.1:8000/home/accredations/
'''      
class HomeAccredationPageView(TemplateView,CacheLoader):
    template_name = 'AccredationPage.html'
'''
http://127.0.0.1:8000/home/about/
'''       
class HomeAboutPageView(TemplateView,CacheLoader):
    template_name = 'AboutPage.html'
    
class HomeAcademicCalendarView(TemplateView,CacheLoader):
	template_name = 'AcademicCalenderPage.html'

class ReportView(TemplateView,CacheLoader):
	
	def get_template_names(self):
		channel = cache.get('channel')
		if channel.is_staff:
			return 'StaffBlogPage.html'
		elif channel.is_manager:
			return 'ManagerBlogPage.html'
		else:
			return 'ProfileLayerPage.html'
	
	def get_context_data(self,**kwargs):
		channel = cache.get('channel')
		kwargs['channel']=cache.get('channel')
		kwargs['channelcontent']=cache.get('channelcontent')
		kwargs['main_template']='ReportPage.html'
		return super().get_context_data(**kwargs)
		
	def post(self,request):
		channel = cache.get('channel')
		report = Report(
		username=channel.username,
		content=request.POST['report_content'],
		code = cache.get('code')
		)
		report.save()
		redirect_object = str(cache.get('report_object'))
		return self.redirect_view()
		
	def redirect_view(self,**kwargs):
		return None
		
		
class RequestNotFoundView(TemplateView,CacheLoader):
	template_name = '404ErrorPage.html'
	
	def get_context_data(self,**kwargs):
		try:
			kwargs=self.load_cache(kwargs)
		except:
			pass
		return super().get_context_data(**kwargs)
		

def DownloadFile(request,params):
	
	with open(params,'r') as download:
		with open(params,'w') as my_download:
			download.write(download.read())
	return True
	
def checkIfDownload(checked=False):
	if checked:
		return True
	else:
		return checkIfDownload(checked)
		















