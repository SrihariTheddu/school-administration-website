''' 
   TRANSACTION APPLICATION
'''

from django.db import models

from Applications.Administration.models import (Channel,Standard)

from django.db.models.signals import (    post_save,
     pre_save,
     pre_delete,
     post_delete,
     pre_init,
     post_init
     )

        
from django.core.signing import Signer


class Transaction(models.Model):
	
	amount = models.FloatField(blank=True)
	
	#student.admision_numbér+month+r
	transaction_code = models.CharField(max_length=40)
	
	paid_on = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.transaction_code
		
def transaction_before_save(instance,sender,**kwargs):
	pass
	
pre_save.connect(transaction_before_save,sender=Transaction)

class TutionFee(models.Model):
	
	reg_number = models.IntegerField()
	
	month = models.CharField(
	max_length=12)
	
	paid = models.BooleanField(default=False)
	
	transaction = models.ForeignKey(
	Transaction,
	on_delete=models.CASCADE,
	blank=True)
	
	def __str__(self):
		return self.transaction.transaction_code
		
	def get_transaction(self):
		'''
		***
		GETTING THE TRANSACTION
		***
		'''
		return self.transaction
	
	def get_transaction_code(self):
		'''
		GETTING THE TRANSACTION CODE
		'''
		return self.transaction.transaction_code
		


class FeeStructure(models.Model):
    
	standard = models.OneToOneField(
	Standard,
	on_delete = models.CASCADE,
	related_name='standard_fee_structure')
	
	exam_fee = models.FloatField()
	
	tution_fee = models.FloatField()
	
	admission_fee = models.FloatField()
	
	def __str__(self):
		return str(self.standard.standard)




class PaymentCard(models.Model):
    
    card_number = models.CharField(max_length=100,unique=True)
    
    tution_fee = models.ManyToManyField(
	TutionFee,
	blank=True)
	
    channel = models.OneToOneField(
	Channel,
	on_delete = models.CASCADE,
	related_name='channel_payment_card')
	
    valid_from = models.DateField(auto_now=False)
	
    valid_to = models.DateField(auto_now=False)
	
    def __str__(self):
	    return self.channel.username
		
		
def payment_card_before_save(instance,sender,**kwargs):
    signer = Signer()
    instance.card_number = signer.sign(instance.channel.username+'@'+str(instance.channel.admission_number))

pre_save.connect(payment_card_before_save,sender=PaymentCard)


class FeeReminder(models.Model):
    
    is_sent = models.BooleanField(default=False)
    
    month = models.CharField(
    max_length=20,unique=True)
    
    sent_at = models.DateTimeField(auto_now=False,null=True)
    
    def __str__(self):
        return self.month
        
        
    