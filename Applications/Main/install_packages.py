from Applications.Administration.models import (
Standard,
Channel
)

from mysite.siteconf import PAYMENT_FORMS

from django.shortcuts import redirect

class BasicAdminPanel:
    
    def __init__(self,*args,**kwargs):
        pass
        
    def CheckStandardView(self):
        try:
            standard= Standard.objects.get(standard=0)
        except:
            Standard.objects.create(standard=0)
        finally:
            return True
            
    def get_standard(self):
    	try:
    		return Standard.objects.get(standard=0)
    	except:
    		return Standard.objects.create(standard=0)
    	
	    
    def CheckManagerView(self,*args,flag=False):
    	if Channel.objects.count()==0:
    		return redirect('Main:AddAdminView')
    	else:
    	    return redirect('Main:HomePage')
    
    def AddAdminView(self):
    	standard = Standard.objects.get_or_create(standard=0)[0]
    	admin = Channel(
    	username='admin',
		father_name = 'superadmin',
		mother_name='superadmin',
		caste='SC',
		language='English',
		key='key',
		email='admin@gmail.com',
		admission_number=0,
		status='MANAGER',
		section='A',
		rollnumber=0,
		mobile_number='0000000000',
		password='password',
		profile=None,
		standard=standard,
		is_manager=True,
		is_staff=False
		)
    	admin.save()
    	return redirect('Main:HomePage')
    	
		
    def install_transactions(self):
        from Applications.Transactions.models import FeeReminder
        for PAYMENT_FORM in PAYMENT_FORMS:
            FeeReminder(
            amount=0,
	        month=PAYMENT_FORM).save()
        return redirect('Main:HomePage')
	
	


			
			
	