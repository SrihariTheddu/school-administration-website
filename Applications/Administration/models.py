''' 
   ADMINISTRATION APPLICATION
'''
from django.db import models

from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    MinValueValidator,
    MaxValueValidator
    )
from django.db.models.signals import (    post_save,
     pre_save,
     pre_delete,
     post_delete,
     pre_init,
     post_init
     )

from django.core.signing import Signer

from Applications.Core.Connector import connector

from Applications.Core.mailing_context import ADMISSION_SUCCESS_MAIL

from datetime import datetime

from django.shortcuts import (
            render,
            redirect,
            reverse
            )
            
from django.urls import (
                        reverse,
                        reverse_lazy
                          )
                          
from django.core.cache import cache

from django.contrib import messages


from mysite.siteconf import (
            MODEL_LANGUAGES,
            MODEL_CASTES,
            MODEL_SECTIONS,
            MODEL_PAYMENT_FORMS,
            CONTRACT_VALIDATION,
            FEE_STRUCTURE,
            PAYMENT_FORMS,
            MODEL_STATUS_OPTIONS,
            MODEL_TC_STATUS,
            MODEL_ADMISSION_STATUS,
            UPLOAD_PROFILE,
            
            
)



from django.core.signing import Signer



                          
from django.core.cache import cache

from django.contrib import messages



#-----------------------------------
#ApplicationForm
class Channel(models.Model):
    
    username = models.CharField(max_length=40,unique=True,
    editable=True,
	validators=[
	     MaxLengthValidator(
	     15,
	     message='Username is too long'
	     ),
	     MinLengthValidator(
	     6,
	     message='Username is too short..')
	]
	)
	
	
    father_name = models.CharField(max_length=50)
	
    mother_name = models.CharField(max_length=50)
	
    caste = models.CharField(
	max_length=50,choices=MODEL_CASTES)
	
    key = models.CharField(
	max_length=100,unique=True)
	
    profile = models.ImageField(upload_to=UPLOAD_PROFILE,max_length=300,blank=True,null=True)
	
    email = models.EmailField(
	max_length=200)
	
    admission_number = models.CharField(max_length=10,blank=True,primary_key=True)
	
    status = models.CharField(
	max_length=20,choices=MODEL_STATUS_OPTIONS)
	
    is_staff= models.BooleanField(default=False)
	
    standard = models.ForeignKey(
	'Standard',
	on_delete=models.CASCADE,
	related_name='standard_students',null=True)
	
    section = models.CharField(max_length=1,
	choices=MODEL_SECTIONS)
	
    rollnumber = models.IntegerField(blank=True)
    
    mobile_number = models.CharField(max_length=20,editable=True,
    validators=[
	     MaxLengthValidator(
	     12,
	     message='Too Long'
	     ),
	     MinLengthValidator(
	     10,
	     message='too short..')
	]
    )
    
    language = models.CharField(
    max_length=50,choices=MODEL_LANGUAGES)
    
    date_of_join = models.DateField(auto_now=True)
    
    is_manager = models.BooleanField(
    default=False)
    
    password = models.CharField(
    max_length=10,default='password',editable=True)
    
    def __str__(self):
        return self.username
	
    def change_password(self,newpassword):
    	'''
    	changing the password of the
    	user
    	'''
    	self.password = newpassword
    	self.save()
	
    def get_absolute_url(self,**kwargs):
    	'''
    	getting the absolute url.of
    	the page...
    	
    	'''
    	return redirect('Main:IndexPage',pk=self.pk)
		
    def get_payment_card(self):
    	'''
    	getting the fee payment card
    	available for the channel
    	'''
    	return self.channel_payment_card
		
    def get_fee_structure(self):
        '''
        getting the fee stuctutre of the channel....
        
        '''
        return self.standard.standard_fee_structure
        
        
    def get_channel_content(self):
    	'''
    	getting the channelcontent
    	'''
    	from Applications.Main.models import (ChannelContent,StaffChannelContent)
    	
    	if self.is_staff:
    		
    		return StaffChannelContent.objects.get(username=self.username)
    		
    	else:
    		
    		return ChannelContent.objects.get(username=self.username)
    		
    	
    	
        
    def get_progress_card(self):
    	'''
    	getting the channel progress card....
    	
    	'''
    	from Applications.Examination.models import FinalResult
    	return FinalResult.objects.get(student=self)
    	
    def get_progress_card_pk(self):
    	'''
    	getting the channel progress card....
    	
    	'''
    	from Applications.Examination.models import FinalResult
    	return FinalResult.objects.get(student=self).pk
   
    def get_standard(self):
    	'''
    	getting the standard of channel
    	'''
    	return self.standard
    
    def get_registered_courses(self):
    	'''
    	get the registered courses
    	of the channel
    	
    	'''
    	return self.channel_courses.all()
    	
    	
    def get_incharge_standard(self):
    	'''
    	getting the channel incharge
    	'''
    	if self.is_staff:
    		return self.standard_incharge.all()[0]
    		
    
    def get_tc_form(self):
    	return self.channel_TCForm.all()[0]
    	
    
    def get_mobile_form(self):
    	return self.change_mobile_number.all()[0]
    	
    
    def get_feedback(self):
    	return self.channel_feedback.all()[0]
    	
    
    def get_appointment(self):
    	return self.channel_appointment.all()[0]
    	
    	
    def get_staff_courses(self):
    	'''
    	getting the channel courses
    	'''
    	if self.is_staff:
    		return self.channel_courses.all()



'''
Intilizing the channel with the required stuff related to the content
.

'''	
def before_save(instance,sender,**kwargs):
	'''
	intilization of the channel content
	'''
	signer = Signer()
	instance.key = signer.sign(instance.username)
	'''
	intilizing the roll number
	'''
	instance.roll_number = instance.standard.standard_students_count()+1  
	instance.admission_number = Channel.objects.count()+1
	if instance.roll_number<50:
		instance.section= 'B'
	else:
		instance.section = 'A'
	'''
	setting the password of the user
	'''
	instance.password = instance.username+str(instance.admission_number)
	
	    
   
'''
making all the students requirements
possible
	
'''	
def after_save(instance,sender,**kwargs):
	'''Importing the requirements'''
	from Applications.Transactions.models import (PaymentCard,TutionFee,Transaction)
	from Applications.Main.models import (ChannelContent,StaffChannelContent)
	from Applications.Examination.models import FinalResult
	
	if instance.is_staff==False:
		
		'''
		***
		CREATING THE CHANNEL CONTENT
		***
		'''
		channelcontent = ChannelContent(
		    username=instance.username,
		    key=instance.key,
		    standard=instance.standard.standard)
		'''
		***
		CREATING THE PROGESS CARD
		'''
		finalresult = FinalResult(
          student=instance,
          is_promoted=False,
          percentage=0,
          gpa='0'
          )
          
	else:
	    '''
	    ***
	    CREATING THE STAFFCHANNELCONTEMT
	    **
	    '''
	    channelcontent = StaffChannelContent(
	    username=instance.username,
	    key=instance.key,
	    standard=instance.standard.standard)
	    
	'''
	***
	CREATING THE PAYMENT CARD
	***
	'''
	fee_card = PaymentCard(
        channel=instance,
        valid_from=datetime(2020,6,20),
        valid_to=datetime(2021,6,20),card_number=instance.admission_number)
        
	try:
		
		if instance.is_staff:
			channelcontent.save()
			fee_card.save()
		else:
			channelcontent.save()
			fee_card.save()
			finalresult.save()
	except:
		RETURN_STR = 'FAILED TO CREATE FEE PAYMENT CARD'
	
	'''
	****
	CREATING THE TUTION FEES 
	TRANSACTIONS
	***
	'''
	for index,form in enumerate(PAYMENT_FORMS):
		
		transaction=Transaction(
		amount=0,
		transaction_code = str(instance.admission_number)+form[0:4]+str(index)
		)
		transaction.save()
		tution_fee = TutionFee(month=form,reg_number=instance.admission_number)
	    
		tution_fee.transaction = transaction
	    
		tution_fee.save()
		fee_card.tution_fee.add(tution_fee)
	    
	'''
	*** 
	CREATING THE MANAGER
	***
	'''    
	if instance.is_manager:
	    Manager(
	    channel=instance
	    ).save()
	    
	    'MANAGER CREATED SUCCESSFULLY'
	
	'''
	***
	SENDING THE MAIL
	***
	'''
	try:
		connector.server()
		
		connector.connect(instance.email)
		
		connector.mailformat(
ADMISSION_SUCCESS_MAIL['Subject'],
ADMISSION_SUCCESS_MAIL['Body'].format(instance.username,instance.admission_number,instance.password,instance.pk),
ADMISSION_SUCCESS_MAIL['Image'],	ADMISSION_SUCCESS_MAIL['Document']
	)
	
		connector.sendmail()
		
		'MAIL SENT SUCCESSFULLY'
		
	except:
		
		'COULD NOT SEND THE MAIL'
		
	
        

'''
Deleting the Channel and the 
respexted allies of the channel
  
'''  
def after_delete(instance,sender,**kwargs):
	'''
	***
	DELETING THE CHANNEL CONTENT
	***
	'''
	try:
		
		instance.get_channel_content().delete()
		
		'CHANNELCONTENT DELETED SUCCESSFULLY'
		
	except:
		
		'CAN NOT DELETE CHANNELCONTENT'
	

	
	'''
	***
	DELETING THE PAYMENT CARD
	***
	'''
	try:
		
		instance.get_payment_card().delete()
		
		'PAYMENT CARD DELETED SUCCESSFULLY...'
	
	except:
		
		'CAN NOT DELETE PAYMENT CARD'
	
	'''
	***
	DELETING THE FINAL RESULT
	***
	'''
	try:
		
		instance.get_progress_card().delete()
		
		'PROGRESS CARD DELETED SUCCESSFULLY'
		
	except:
		
		'CAN NOT DELETE PROGRESS CARD'
    

	
'''
****
ADDING THE EXTRA FEATURES TO THE MODEL
****
'''	
post_save.connect(after_save,sender=Channel)	
	
pre_save.connect(before_save,sender=Channel)		

post_delete.connect(after_delete,sender=Channel)



        
#-----------------------------------
#StandardModel	
class Standard(models.Model):
	
	standard = models.IntegerField(unique=True)
	
	incharge = models.ForeignKey(
	Channel,
	on_delete=models.CASCADE,
	related_name='standard_incharge',blank=True,null=True,editable=True)
	
	def __str__(self):
		return str(self.standard)
		
	def get_students(self):
		'''
		getting the all students of
		the standard
		'''
		return self.standard_students.all()
		
	def get_courses(self):
		'''
		getting all the courses  of the standard
		'''
		return self.standard_courses.all()
	    
	def get_groupchat(self):
		'''
		getting the groupchat page
		'''
		return self.standard_groupchat
		
	def get_fee_structure(self):
		return self.standard_fee_structure.all()[0]
		
	def get_standard_notifications(self):
		return self.standard_notifications.all()
		
	def standard_students_count(self):
	    return len(self.standard_students.all())
		
	
	
	
	    


def standard_model_after_save(instance,sender,**kwargs):
	
	'''
	***
	CREATING THE GROUP CHAT
	***
	'''
	from Applications.DashBoard.models import (GroupChat)
	
	group = GroupChat(
	    standard=instance,
	    created_on=datetime.today()
	    )
	'''
	***
	CREATING THE FEE STRUCTURE
	***
	'''
	from Applications.Transactions.models import FeeStructure
	
	dict_obj = FEE_STRUCTURE[instance.standard]
	
	fee_structure = FeeStructure(
	    standard=instance,
	    exam_fee=dict_obj['Exam Fee'],
	    admission_fee = dict_obj['Admission Fee'],
	    tution_fee = dict_obj['Tution Fee']
	    )
	 
	try:
		
		group.save()
		
		fee_structure.save()
		
	except:
		
		'COULD NOT SAVE FEE STRUCTURE'
	    

post_save.connect(standard_model_after_save,sender=Standard)

			
									
class Department(models.Model):
	
	head = models.ForeignKey(
	Channel,
	on_delete=models.CASCADE,
	related_name='head_of_department',
	null=True
	)
	
	title = models.CharField(max_length=100)
	
	members = models.ManyToManyField(
	Channel,
	related_query_name='all_members',blank=True)
	
	vision = models.CharField(max_length=300)
	
	message = models.CharField(max_length=150)
	
	def __str__(self):
		return self.title
		
		
	def change_head(self,channel):
		'''
		
		changing the head of the
		channel of the department
		
		
		'''
		self.head = channel
		self.save()
		
		
	def get_posted_circulars(self):
		'''
		***
		GETTING THE POSTED CIRCULARS
		***
		'''
		return self.posted_circulars.all()
		
		
#-----------------------------------
#TransferCertificateForm....		
class TCForm(models.Model):
	
	channel = models.ForeignKey(
	Channel,
	on_delete=models.CASCADE,
	related_name = 'channel_TCForm')
	
	reason = models.TextField(max_length=500,editable=True)
	
	applied_on = models.DateField(auto_now=True)
	
	granted = models.BooleanField(
	default=False)
	
	status = models.CharField(
	max_length=40,choices=MODEL_TC_STATUS)
	
	fee_section = models.BooleanField(default=False)
	
	
	
	def __str__(self):
		return self.channel.username +' with '+self.channel.admission_number
		
	def submit(self,**kwargs):
		'''
		Granting the TCForm
		'''
		self.granted = True
		'''
		***
		SENDING THE MAIL
		***
		'''
		try:
			
			self.save()
			
			connector.server()
			
			connector.connect(instance.email)
			
			connector.mailformat(
ADMISSION_SUCCESS_MAIL['Subject'],
ADMISSION_SUCCESS_MAIL['Body'].format(instance.username,instance.admission_number,instance.password,instance.pk),
ADMISSION_SUCCESS_MAIL['Image'],	ADMISSION_SUCCESS_MAIL['Document']
)
			connector.sendmail()
			
			'MAIL SENT SUCCESSFULLY'
			
		except:
			
			'COULD NOT SEND THE MAIL'
		
	
		
		
		
		
		
		
		
class AdmissionForm(models.Model):
    
    reg_number = models.CharField(max_length=10,unique=True)
    
    fullname = models.CharField(max_length=50)
    
    father_name = models.CharField(max_length=50)
    
    status = models.CharField(max_length=50,choices=MODEL_ADMISSION_STATUS,default='APPLIED',editable=True
    )
    
    email_id  = models.EmailField(max_length=50)
    
    mobile_number = models.CharField(max_length=20)
    
    standard = models.IntegerField()
    date = models.DateField(auto_now=True)
    
    approved = models.BooleanField(default=False)
    
    msg_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return self.reg_number
        
    def save(self):
    	super().save()
    	Manager.objects.get(channel=Channel.objects.get(username='admin')).admission_forms.add(self)
    	
class ChangeMobileNumberForm(models.Model):
    
    channel = models.ForeignKey(
    Channel,
    on_delete = models.CASCADE,
    related_name = 'change_mobile_number')
    
    reason = models.TextField(max_length=500,editable=True)
    
    
    new_number = models.TextField(
    max_length=500,editable=True)
    
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.channel.username+' admission  '+self.channel.admission_number
        
    def verified(self):
    	'''
    	Changing the mobile number
    	'''
    	self.channel.mobile_number=self.new_number
    	self.is_verified=True
    	self.channel.save()
    	self.save()
        
        
class FeedBack(models.Model):
    
    channel = models.ForeignKey(
    Channel,
    on_delete = models.CASCADE,
    related_name = 'channel_feedback')
    
    feedback = models.TextField(
    max_length=500,editable=True)
    
    on = models.DateTimeField(
    auto_now=True
    )
    
    is_drafted = models.BooleanField(default=False)
    
    reply_text = models.TextField(
    max_length=500,blank=True,null=True)
    
    def __str__(self):
        return self.channel.username
        
        
class Appointment(models.Model):
    
    channel = models.ForeignKey(
    Channel,
    on_delete = models.CASCADE,
    related_name = 'channel_appointment')
    
    reason = models.TextField(
    max_length=500,editable=True)
    
    on_date = models.DateField(
    auto_now=False)
    
    session = models.CharField(
    max_length=40)
    
    applied_on = models.DateTimeField(
    auto_now=True
    )
    
    success = models.BooleanField(default=False)
    
    msg_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return self.channel.username
        
    def granted(self):
    	'''
    	***
    	CREATING THE MESSAGE ON
    	***
    	'''
    	from Applications.DashBoard.models import IndividualMessage
    	
    	IndividualMessage(
    	send_to=self.channel,
    	code='IM'+str(self.channel[0:2]).upper()+str(IndividualMessage.objects.count()),
    	title = 'Appointement Granted',
    	message=f'You have applied for appointment on {self.on_date} at the {self.session}.\nYou are here by to attend the meetings 15 minutes earlier to avoid any kind of inconvenience.\nWe are glad to meet make a interactive session regrading the issue brought up by you\n\n\n\t\t\tWith Regards\n\t\t\t\tFrom Staff'
    	).save()
    	
    	
		
class Manager(models.Model):
    
    channel = models.OneToOneField(
    Channel,
    on_delete=models.CASCADE
    )
    
    admission_forms = models.ManyToManyField(
    AdmissionForm,
    blank=True
    )
    
    tc_forms = models.ManyToManyField(
    TCForm,
    blank=True)
    
    cm_forms = models.ManyToManyField(
    ChangeMobileNumberForm,
    blank=True
    )
    
    def __str__(self):
        return self.channel.username
        
