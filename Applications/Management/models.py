''' 
   MANAGEMENT APPLICATION
'''

from django.db import models

from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    MinValueValidator,
    MaxValueValidator
    )



from Applications.Administration.models import (Standard,Channel)

from mysite.siteconf import UPLOAD_POSTURES


from datetime import datetime 
               
class EventRegister(models.Model):
	
	username = models.CharField(max_length=100)
	
	standard = models.ForeignKey(
	Standard,
	on_delete=models.CASCADE,
	related_name='standard_events')
	
	admission_number = models.IntegerField()
	
	this_event = models.ForeignKey(
	'Event',
	on_delete=models.CASCADE,
	related_name='event_to_register')
	
	def __str__(self):
		return self.username
    
	
               
class Event(models.Model):
	
	event = models.TextField(max_length=200)
	
	vision = models.TextField(max_length=500)
	
	
	date = models.DateTimeField(auto_now=False)
	
	management = models.ForeignKey(
	'Management',
	on_delete=models.CASCADE,
	related_name='events')
	
	image = models.ImageField(upload_to=UPLOAD_POSTURES,max_length=400,blank=True,null=True)
	
	participents = models.ManyToManyField(
	EventRegister,blank=True)
	
	def __str__(self):
		return self.event
		
	def modified_vision(self):
		str_format = str(self.vision)
		return str_format[0:50]
	
	def is_open(self):
		now = datetime.today()
		this_date = self.date.date
		if this_date>now:
			return True
		else:
			return False
			
	def check_user_registered(self,username):
		try:
			print(self.participents.get(username=username))
			return True
		except:
			return False
		
		
	

class Management(models.Model):
	
	name = models.CharField(max_length=100)
	
	head = models.ForeignKey(
    Channel,
    on_delete = models.CASCADE,
    related_name="head_of_management")
    
	
    
	co_ordinaters = models.ManyToManyField(
    Channel,
    related_query_name='co-ordinators_in_management')
    
	def __str__(self):
		return self.name
		
	def get_events(self):
		return self.events.all()
    	
    	
class Player(models.Model):
	
	student = models.ForeignKey(
	Channel,
	on_delete = models.CASCADE)
	
	game = models.CharField(max_length=40,null=True)
	
	sport = models.CharField(max_length=40,null=True)
	
	is_captain = models.BooleanField(default=False)
	
	is_vice_captain = models.BooleanField(default=False)
	
	def __str__(self):
	    return self.student.username
	    
	def add_to_team(self):
	    SchoolTeam.objects.get(sport=self.sport).add(self)
    	
class SchoolTeam(models.Model):
    
    sport = models.CharField(
    max_length=100)
    
    vision = models.TextField(
    max_length=500)
    
    coach = models.ForeignKey(
    Channel,
    on_delete = models.CASCADE,
    related_name="coach")
    
    incharges = models.ManyToManyField(
    Channel,
    related_query_name='incharges_of_team',
    blank = True)
    
    
    players = models.ManyToManyField(
    Player,
    related_query_name='co-ordinators_in_management')
    
    password = models.CharField(
	max_length=12,
	validators=[
	     MaxLengthValidator(
	     11,
	     message='Your Mobile Number is Too Long'
	     ),
	     MinLengthValidator(
	     8,
	     message='Your Mobile Number is too short..')
	]
	)
    def __str__(self):
    	return self.sport
    	
    def get_players(self):
        return self.players.all()
        
    def get_captain(self):
        return self.players.get(is_captain=True)
        
    def get_vice_captain(self):
        return self.players.get(is_vice_captain=True)
        

class Report(models.Model):
    
    admission_number = models.IntegerField()
    
    content = models.TextField(max_length=500)  
    
    reported_on=models.DateTimeField(auto_now=True)
    
    code = models.CharField(max_length=20)
    
    def __str__(self):
        return self.content	
    	

	

