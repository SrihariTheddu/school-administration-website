from django.shortcuts import (
        render,
        redirect
        )
from django.urls import (reverse_lazy,reverse)

from Applications.DashBoard.models import (
          Notification,
          Circular,
          Reminder,
          GroupChat,
           Chat,
           IndividualMessage
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

def get_context_model(code):
	if code[0:2]=='NT':
		return Notification.objects.get(code=code)
	elif code[0:2]=='RM':
		return Reminder.objects.get(code=code)
	elif code[0:2]=='CR':
		return Circular.objects.get(code=code)
	else:
		return False
		
def get_context_model_queryset(channelcontent,code,df=False):
	if code[0:2]=='NT':
		if df:
			return channelcontent.df_notifications
		else:
			return channelcontent.notifications
	elif code[0:2]=='RM':
		if df:
			return channelcontent.df_reminders
		else:
			return channelcontent.reminders
	elif code[0:2]=='CR':
		if df:
			return channelcontent.df_circulars
		else:
			return channelcontent.circulars
	elif code[0:2]=='IM':
		if df:
			return channelcontent.df_individual_messages
		else:
			return channelcontent.individual_messages
	else:
		return False

def check_context_in_draft(queryset,context,flag=False):
    for re_context in queryset.all():
        if re_context==context:
            flag=True
            break
    return flag
    

def get_chunk_code(title,df=False):
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
        

#Student related views....
        
class InBoxView(ListView):
	model = Notification
	template_name = 'BlogPage.html'
	context_object_name = 'contexts'
	
	def get_queryset(self,**kwargs):
	    return cache.get('channelcontent').get_all_inbox()
		
		
	def get_context_data(self,**kwargs):
	    kwargs['student']=cache.get('channel')
	    kwargs['channel']=cache.get('channel')
	    kwargs['drafts']=False
	    kwargs['title']='INBOX'
	    kwargs['main_template']='InBoxPage.html'
	    kwargs['side_template']='InBoxSidePage.html'
	    kwargs['createlink']='DashBoard:'
	    return super().get_context_data(**kwargs)
	    

class NotificationListView(ListView):
	model = Notification
	template_name = 'BlogPage.html'
	context_object_name = 'contexts'
	
	def get_queryset(self,**kwargs):
	    return cache.get('channelcontent').notifications.all()
		
		
	def get_context_data(self,**kwargs):
	    kwargs['student']=cache.get('channel')
	    kwargs['channel']=cache.get('channel')
	    kwargs['drafts']=False
	    kwargs['title']='NOTIFICATIONS'
	    kwargs['main_template']='InBoxPage.html'
	    kwargs['side_template']='InBoxSidePage.html'
	    return super().get_context_data(**kwargs)

class ReminderListView(ListView):
	model = Reminder
	template_name = 'BlogPage.html'
	context_object_name = 'contexts'
	
	def get_queryset(self,**kwargs):
	    return cache.get('channelcontent').reminders.all()
		
		
	def get_context_data(self,**kwargs):
	    kwargs['student']=cache.get('channel')
	    kwargs['channel']=cache.get('channel')
	    kwargs['drafts']=False
	    kwargs['title']='REMINDERS'
	    kwargs['main_template']='InBoxPage.html'
	    kwargs['side_template']='InBoxSidePage.html'
	    return super().get_context_data(**kwargs)
		
class CircularListView(ListView):
	model = Circular
	template_name = 'BlogPage.html'
	context_object_name = 'contexts'
	
	def get_queryset(self,**kwargs):
	    return cache.get('channelcontent').circulars.all()
		
		
	def get_context_data(self,**kwargs):
	    kwargs['student']=cache.get('channel')
	    kwargs['channel']=cache.get('channel')
	    kwargs['drafts']=False
	    kwargs['title']='CIRCULARS'
	    kwargs['main_template']='InBoxPage.html'
	    kwargs['side_template']='InBoxSidePage.html'
	    return super().get_context_data(**kwargs)
	    
	    
	
class DraftContextBoxView(ListView):
	model = Notification
	template_name = 'BlogPage.html'
	context_object_name = 'contexts'
	
	def get_queryset(self,**kwargs):
	    return cache.get('channelcontent').get_draft_box()
		
		
	def get_context_data(self,**kwargs):
	    kwargs['student']=cache.get('channel')
	    kwargs['channel']=cache.get('channel')
	    kwargs['drafts']=True
	    kwargs['title']='DRAFTS'
	    kwargs['main_template']='InBoxPage.html'
	    kwargs['side_template']='InBoxSidePage.html'
	    return super().get_context_data(**kwargs)
		
def ContextDetailView(request,code):
	context = get_context_model(code)
	channelcontent = cache.get('channelcontent')
	is_drafted=check_context_in_draft(get_context_model_queryset(channelcontent,code),context)
	return render(request,'BlogPage.html',{'context':context,'is_drafted':is_drafted,'student':cache.get('channel'),'channel':cache.get('channel'),
'main_template':'ContextDetailPage.html',
'side_template':'InBoxSidePage.html'
    })
	


def ClearAllView(request):
	'''
	clearing the inbox contexts
	'''
	channel = cache.get('channelcontent')
	channel.reminders.clear(channel.reminders.filter(is_drafted=False))
	channel.notifications.clear(channel.notifications.filter(is_drafted=False))
	channel.circulars.clear(channel.circulars.filter(is_drafted=False))
	return redirect('DashBoard:InBoxPage')
	
	
	
	
def DeleteContextView(request,code):
	'''
	deleting the related model
	'''
	channelcontent = cache.get('channelcontent')
	context = get_context_model(code)
	context_queryset = get_context_model_queryset(channelcontent,code,df=False)
	context_queryset.remove(context)
	return redirect('DashBoard:InBoxPage')
	
	 
	  
	   
	    
	      
	
	
def AddDraftContextView(request,code):
    channelcontent = cache.get('channelcontent')
    context = get_context_model(code)
    context_queryset = get_context_model_queryset(channelcontent,code,df=True)
    context_queryset.add(context)
    return redirect('DashBoard:InBoxPage')
        
    
def RemoveDraftContextView(request,code):
    channelcontent = cache.get('channelcontent')
    context = get_context_model(code)
    context_queryset = get_context_model_queryset(channelcontent,code,df=True)
    context_queryset.remove(context)
    return redirect('DashBoard:InBoxPage')
        
    
        

def ReplyContextView(request,code):
    issue = request.POST['issue']
    context = get_context_model(code)
    messages.add_message(request,30,'WE WILL REVIEW YOUR ISSUE SOON\nTHANK YOU FOR YOUR FEEDBACK')
    return redirect('DashBoard:ContextDetailPage',pk=context.pk)
        
    
'''
------------------------------------
   GROUP CHAT RELATED VIEWS....
#GroupChatting related views...  
'''	
class GroupChatView(DetailView):
    model = GroupChat
    template_name = 'GroupChatPage1.html'
    context_object_name = 'group'
    
    def get_context_data(self,**kwargs):
        kwargs['student']=cache.get('channel')
        kwargs['channel']=cache.get('channel')
        return super().get_context_data(**kwargs)
    
    
def PostChatView(request,pk):
    message = request.POST['message']
    document = request.POST['document']
    student = cache.get('channel')
    chat = Chat(
            sender=student.username,
            document=document,
            message=message,
            standard=student.standard.standard
            )
    chat.save()
    group = GroupChat.objects.get(standard=student.standard)
    result = group.post(chat)
    return redirect('DashBoard:GroupChatPage',pk=group.pk)
    

class MyChatsView(ListView):
    model = Chat
    template_name = 'MyChatPage.html'
    context_object_name = 'chats'
    
    def get_queryset(self):
    	return Chat.objects.filter(sender=cache.get('channel').username)
    
    def get_context_data(self,**kwargs):
        kwargs['student']=cache.get('channel')
        kwargs['channel']=cache.get('channel')
        return super().get_context_data(**kwargs)
    
    
class GroupMembersView(DetailView):
    model = GroupChat
    template_name = 'GroupMembersPage.html'
    context_object_name = 'group'
    
    def get_context_data(self,**kwargs):
        kwargs['student']=cache.get('channel')
        kwargs['channel']=cache.get('channel')
        kwargs['media']=False
        return super().get_context_data(**kwargs)
        

class GroupMediaView(DetailView):
    model = GroupChat
    template_name = 'GroupMembersPage.html'
    context_object_name = 'group'
    
    def get_context_data(self,**kwargs):
        kwargs['student']=cache.get('channel')
        kwargs['channel']=cache.get('channel')
        kwargs['media']=True
        kwargs['chats']=self.object.chats.filter(standard=self.object.standard.standard,is_document=True)
        return super().get_context_data(**kwargs)
        
        
def DeleteChatView(request,pk):
    chat = Chat.objects.get(pk=pk,sender=cache.get('channel').username)
    
    

 
'''
------------------------------------
   STAFF RELATED VIEWS....
#views...  
'''	

#reminders related....
class StaffReminderCreateView(TemplateView):
    template_name = 'StaffBlogPage.html'
    
    def get_context_data(self,**kwargs):
        channelcontent = cache.get('channelcontent')
        kwargs['channelcontent']=cache.get('channelcontent')
        kwargs['channel']=cache.get('channel')
        kwargs['main_template']='ContextCreatePage.html'
        kwargs['code']='RM'+str(cache.get('channel').standard.standard)+str(Reminder.objects.count())
        kwargs['sender']=cache.get('course')
        kwargs['date_field']=True
        return super().get_context_data(**kwargs)
        

    def post(self,request):
        title = request.POST['title']
        message = request.POST['message']
        date=request.POST['deadline']
        
        code='RM'+str(cache.get('channel').standard.standard)+str(Reminder.objects.count())+str(get_chunk_code(title))
        reminder = Reminder(
        code=code,
        sender=cache.get('course'),
        title=title,
        message=message,
        last_date=date
        )
        reminder.save()
        return redirect('DashBoard:StaffContextDetailPage',code=reminder.code)




class StaffReminderListView(ListView):
    model = Reminder
    template_name = 'StaffBlogPage.html' 
    context_object_name = 'contexts'
    
    def get_queryset(self):
        return self.model.objects.filter(sender=cache.get('course'))
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='StaffInBoxPage.html'
        kwargs['channelcontent']=cache.get('channelcontent')
        kwargs['channel']=cache.get('channel')
        kwargs['channelcontent']=cache.get('channelcontent')
        kwargs['channel']=cache.get('channel')
        kwargs['createlink']='DashBoard:StaffReminderCreatePage'
        kwargs['title']='REMINDERS'
        return super().get_context_data(**kwargs)
    





def StaffReminderDeleteView(request,pk):
    Reminder.objects.get(pk=pk).delete()
    return redirect('DashBoard:StaffReminderListPage')
    




#Notifications related....
class StaffNotificationCreateView(TemplateView):
    template_name = 'StaffBlogPage.html'
    
    def get_context_data(self,**kwargs):
        channelcontent = cache.get('channelcontent')
        kwargs['channelcontent']=cache.get('channelcontent')
        kwargs['channel']=cache.get('channel')
        kwargs['main_template']='ContextCreatePage.html'
        kwargs['title']='NOTIFICATION'
        kwargs['sender']=cache.get('channel').standard
        kwargs['code']='NT'+str(cache.get('channel').standard.standard)+str(Notification.objects.count())
        kwargs['date_field']=False
        return super().get_context_data(**kwargs)
        
    
    def post(self,request):
        title = request.POST['title']
        message = request.POST['message']
        code='NT'+str(cache.get('channel').standard.standard)+str(Notification.objects.count())+str(get_chunk_code(title))
        notification = Notification(
        code=code,
        sender=cache.get('channel'),
        standard=cache.get('channel').standard,
        title=title,
        message=message,
        )
        notification.save()
        return redirect('DashBoard:StaffContextDetailPage',code=notification.code)



class StaffNotificationListView(ListView):
    model = Notification
    template_name = 'StaffBlogPage.html' 
    context_object_name = 'contexts'
    
    def get_queryset(self):
        return self.model.objects.filter(standard=cache.get('channel').standard)
    
    def get_context_data(self,**kwargs):
        kwargs['main_template']='StaffInBoxPage.html'
        channelcontent = cache.get('channelcontent')
        kwargs['createlink']='DashBoard:StaffNotificationCreatePage'
        kwargs['channelcontent']=cache.get('channelcontent')
        kwargs['channel']=cache.get('channel')
        kwargs['title']='NOTIFICATIONS'
        
        return super().get_context_data(**kwargs)
    



def StaffContextDetailView(request,code):
	context = get_context_model(code)
	json_context = {
	'context':context,
	'main_template':'StaffContextDetailPage.html',
	'channelcontent':cache.get('channelcontent'),
	'channel':cache.get('channel')
	}
	return render(request,'StaffBlogPage.html',json_context)

def StaffContextDeleteView(request,code):
    context = get_context_model(code)
    context.delete()
    if code[0:2]=='NT':
        return redirect('DashBoard:StaffNotificationListPage')
    else:
        return redirect('DashBoard:StaffReminderListPage')
    





    