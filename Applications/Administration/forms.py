from django import forms

from Applications.Administration.models import (
                Channel,
                TCForm
                )
 

                              
class ApplicationForm(forms.Form):
	
	fullname = forms.CharField(max_length=50)
	
	fathername = forms.CharField(max_length=50)
	
	mobile = forms.CharField(max_length=12)
	
	email = forms.EmailField(max_length=50)
	
	standard = forms.IntegerField()
	
	grade = forms.FloatField()
	
	
	
	

class ChannelForm(forms.ModelForm):
	
	class Meta:
		
		model = Channel
		fields = '__all__'
	    
class TCFormClass(forms.ModelForm):
    
    class Meta:
        model = TCForm
        fields = ['reason']