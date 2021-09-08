from django.db import models

from Applications.Administration.models import  (
                 Department,
                 Standard,
                 Channel
                 )
                 
from Applications.Education.models import  (
         Course,
         )

         
from mysite.siteconf import UPLOAD_DOCUMENTS


class BaseModel(models.Model):
	
	code = models.CharField(max_length=10,unique=True)
	
	sent_at = models.DateTimeField(auto_now=True)
	
	title = models.CharField(max_length=100)
	
	message = models.TextField(max_length=600)
	
	
	
	class Meta:
		abstract = True
		
	def __str__(self):
		return self.title
		
	
	
class Circular(BaseModel):
	
	sender = models.ForeignKey(
	Department,
	on_delete=models.CASCADE,
	related_name = 'posted_circulars')
	
	
	def save(self):
	    super().save()
	    '''
	    ***
	    SENDING TO ALL STUDENTS
	    ***
	    '''
	    for cc in Channel.objects.all():
	        cc.get_channel_content().circulars.add(self)
	    
	
	
	
	
	
	    	
	
	
	
		

class Notification(BaseModel):
	
	sender = models.ForeignKey(
	Channel,
	on_delete=models.CASCADE,
	related_name='posted_notifications')
	
	standard = models.ForeignKey(
	Standard,
	on_delete=models.CASCADE,
	related_name='standard_notifications')
	
	def save(self):
	    super().save()
	    '''
	    ***
	    SENDING TO THE STUDENST
	    ***
	    '''
	    for channel in self.standard.standard_students.all():
	        channel.get_channel_content().notifications.add(self)
	
	
	
	    
	
	
class Reminder(BaseModel):
	
	sender = models.ForeignKey(
	Course,
	on_delete=models.CASCADE,
	related_name='course_reminders')
	
	last_date = models.DateTimeField(auto_now=False)
	
	def save(self):
		'''
		CODING THE CONTEXT
		'''
		self.code='RM'+str(Reminder.objects.count())
		super().save()
		'''
		***
		SENDING THE REMINDER FOR 
		REGISTERED STUDENTS...
		***
		'''
		for channel in self.sender.get_registered_students():
			channel.get_channel_content().reminders.add(self)
	
	
	
	def send(self):
		'''
		***
		SENDING THE REMINDER
		**
		'''
		self.code='RM'+str(Reminder.objects.count())
		self.save()
	    
	    
	        
class IndividualMessage(BaseModel):
    
    sender = models.ForeignKey(
    Channel,
    on_delete = models.CASCADE,
    related_name='channel_messages')
    
    def send(self):
    	'''
    	***
    	SETTING THE CODE FOR IM
    	***
    	'''
    	self.code = 'IM'+str(IndividualMessage.objects.count())
    	self.save()
    	'''
    	***
    	SENDING TO THE USER
    	***
    	'''
    	self.sender.get_channel_content().individual_messages.add(self)
    	
    	
	        
	        
class Chat(models.Model):
    
    is_document = models.BooleanField(default=False)
    
    standard = models.IntegerField(default=0)
   
    sender = models.CharField(max_length=40)
    
    message = models.TextField(
    max_length=500,blank=True,null=True)
    
    document = models.FileField(upload_to=UPLOAD_DOCUMENTS,max_length=500,blank=True,null=True)
    
    sent_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.message:
            return self.sender+' ' +self.message
        else:
            return self.sender+' : ' +str(self.document.path)
    
    def save(self):
    	'''
    	***
    	SAVING THE MESSAGE
    	***
    	'''
    	if self.message:
    		self.is_document=False
    	else:
    		self.is_document=True
    	super().save()
    
        
        
class GroupChat(models.Model):
    
    standard = models.OneToOneField(
    Standard,
    on_delete = models.CASCADE,
    related_name='standard_groupchat')
    
    
    chats = models.ManyToManyField(
    Chat,
    blank=True)
    
    created_on = models.DateTimeField(
    auto_now=True)
    
    
    def __str__(self):
        return str(self.standard.standard)
    
    def get_group_admin(self):
    	'''
    	GETTING THE GROUP ADMIN
    	'''
    	return self.standard.incharge.get_fullname()
        
    def get_students(self):
    	'''
    	GETTING THE GROUP MEMBERS
    	'''
    	return self.standard.standard_students.all()
    
    def get_channels(self):
    	'''
    	GETTING THE CHANNELCONTENTS
    	'''
    	channel_contents = []
    	for channel in self.get_students():
    		channel_contents.append(channel.get_channel_content())
    	return channel_contents
        	
        
    def clear_chats(self):
    	'''
    	CLEARING ALL THE CHATS
    	'''
    	self.chats.clear()
    	
        
    def get_media(self):
    	'''
    	GETTING THE GROUP MEDIA
    	'''
    	return Chat.objects.filter(document!=None,standard=self.standard)
        
    def post(self,chat):
    	'''
    	POSTING THE CHAT
    	'''
    	try:
    		self.chats.add(chat)
    		return True
    	except:
    		return False
            
    
    
