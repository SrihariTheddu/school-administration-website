from django.shortcuts import render

from Applications.Transactions.models import (
            Transaction,
            TutionFee,
            PaymentCard,
            FeeStructure,
            )
from Applications.Administration.models import (
                Channel
                )   
from django.core.cache import cache


from django.views.generic import (
      DetailView,
      ListView,
      TemplateView
      )

from django.contrib import messages

from Applications.Core.loader import CacheLoader


class FeeStructureView(ListView,CacheLoader):
	model = FeeStructure
	template_name = 'FeeStructurePage.html'
	context_object_name = 'feestructures'
	
	def get_context_data(self,**kwargs):
	    kwargs = self.load_cache(kwargs)
	    return super().get_context_data(**kwargs)
		

class FeePaymentCardView(DetailView,CacheLoader):
	model = PaymentCard
	template_name = 'FeePaymentCardPage.html'
	context_object_name = 'card'
	
	def get_context_data(self,**kwargs):
	    kwargs = self.load_cache(kwargs)
	    return super().get_context_data(**kwargs)


class PaymentFormView(DetailView,CacheLoader):
	model = Transaction
	template_name = 'TransactionPage.html'
	context_object_name = 'transaction'
	
	def get_context_data(self,**kwargs):
	    kwargs = self.load_cache(kwargs)
	    return super().get_context_data(**kwargs)
		
		
		
class TransactionOnSuccessView(DetailView,CacheLoader):
	model = Transaction
	template_name = 'TransactionOnSuccessPage.html'
	context_object_name='transaction'
	
	def get_context_data(self,**kwargs):
	    kwargs = self.load_cache(kwargs)
	    return super().get_context_data(**kwargs)
		
	
	
class TransactionOnFailureView(DetailView,CacheLoader):
	model = Transaction
	template_name = 'TransactionOnFailurePage.html'
	context_object_name='transaction'
	
	def get_context_data(self,**kwargs):
	    kwargs = self.load_cache(kwargs)
	    return super().get_context_data(**kwargs)
		
	
	
class TransactionDetailView(DetailView,CacheLoader):
	model = Transaction
	template_name = 'TransactionDetailPage.html'
	context_object_name='transaction'
	
	def get_context_data(self,**kwargs):
	    return super().get_context_data(**kwargs)


class TransactionIndexView(TemplateView,CacheLoader):
    template_name = 'TransactionIndexPage.html'
    
    def get_context_data(self,**kwargs):
        channel = cache.get('channel')
        student = Channel.objects.get(username=channel.username)
        kwargs['card']=student.get_payment_card()
        kwargs['feestruct']=student.get_fee_structure()
        kwargs['channel']=cache.get('channel')
        kwargs['student']=cache.get('channel')
        return super().get_context_data(**kwargs)
		



	