from django import forms

from Applications.Education.models import (
        PostAssignment,
        AssignmentDocument,
        PostTutorial,
        )
        
        
class PostAssignmentForm(forms.ModelForm):
	class Meta:
		model = PostAssignment
		fields = '__all__'
		

class PostTutorialForm(forms.ModelForm):
	class Meta:
		model = PostTutorial
		fields = '__all__'