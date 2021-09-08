
#Importing the Required modules..

from matplotlib import pyplot as plt
import numpy as np
from Applications.Administration.models import Standard
from Applications.Education.models import Course,PostAssignment
from Applications.Examination.models import CourseResult
from mysite.siteconf import (
STANDARD_STRENGTH_ANIMATIONS,
MANAGER_RESULTS_ANIMATIONS,
MESSAGES_VIEWED_ANIMATIONS

)



#Write Your Code Here...
class Animation:
	
	def __init__(self):
		self.rows = []
		self.columns = []
		self.color_set = [
		'red','green','blue','yellow','cyan','orange','pink','violet','white','black'
		]
		self.animation_file = STANDARD_STRENGTH_ANIMATIONS['BAR_GRAPH']
		self.animation_pie_file = STANDARD_STRENGTH_ANIMATIONS['PIE_GRAPH']
		self.plt = plt
		self.colors = []
		
	def set_rows(self,rows):
		self.rows = rows
		return self.rows
		
	def set_colors(self):
		for index in range(0,len(self.rows)):
			self.colors.append(self.color_set[index])
			
		
	def set_columns(self,columns):
		self.columns = columns
		return self.columns
		
	def check_match(self):
		if len(self.rows)==len(self.columns):
			return True
		else:
			return False
			
	def set_labels(self,x_label=None,y_label=None,title=None):
		self.plt.xlabel(x_label)
		self.plt.ylabel(y_label)
		self.plt.title(title)
		
	def set_bar(self):
		self.set_colors()
		self.plt.bar(self.columns,self.rows,color=self.colors)
		
	def set_graph(self):
		self.plt.bar(self.columns,self.rows,self.color_set[0:len(self.columns)],linewidth=5)
		
		
	def fit_model(self,ANIMATION):
		try:
			if ANIMATION=='BAR':
				self.set_bar()
			else:
				self.set_graph()
			return True
				
		except KeyError as error:
			print(error.args)
			return False
			
	def save_as_image(self):
		self.plt.savefig(self.animation_file)
		
	def show(self):
		self.plt.show()


class FitModel(Animation):
	
	def __init__(self,**kwargs):
		self.course_marks = 0
		super().__init__(**kwargs)
	
	def fix_queryset(self,queryset):
	    self.models = queryset
		
	def get_standard_rows(self,**kwargs):
		for model in self.models:
			self.columns.append(model.standard)
			
	def get_standard_values(self):
		for model in self.models:
			self.rows.append(model.standard_students_count())
			
	def get_marks_values(self):
		for model in self.models:
			self.rows.append(model.present_marks)
		
	def install_sheet(self):
		from DataProcessorSystem.GoogleSheetProcessor.DataBaseModel import  DataBaseModel
		from mysite.siteconf import (
		GOOGLE_SPREADSHEET_NAME,
		CREDENTIALS_PATH
		)
		
		self.marks_sheet = DataBaseModel(GOOGLE_SPREADSHEET_NAME,CREDENTIALS_PATH)
		
	def get_marks_sheet_as_df(self):
		self.marks_sheet_df = self.marks_sheet.DataBaseData
		
	def get_mark_rows(self):
		return self.marks_sheet.getAttributes()[3:]
		
	def fit_marksheet_model(self):
		self.columns = self.get_mark_rows()
		self.rows = self.get_marks_from_sheet()
		self.set_bar()
		
	def fit_passed_students_model(self):
	    self.columns = self.get_mark_rows()
	    self.get_marks_sheet_as_df()
	    self.rows = self.filter_passed()
	    
	    
	def get_marks_from_sheet(self):
		self.get_marks_sheet_as_df()
		self.course_marks = list(self.marks_sheet_df.sum())[1:-2]
		return self.course_marks
		
	def filter_passed(self):
		passed_students_count =[]
		for col,row in zip(range(0,len(list(self.marks_sheet_df.columns)[3:])),list(self.marks_sheet_df.count())[1:-2]):
			sub_passed=0
			for inner_row in range(0,row):
				if self.marks_sheet_df.iloc[inner_row][col]>25:
					sub_passed+=1
			passed_students_count.append(sub_passed)
		return passed_students_count
		
	def get_pass_percentage(self):
		passed_students_count = self.filter_passed()
		total_attempted_students = list(self.marks_sheet.count())[0]
		pass_percentage = (passed_students_count/total_attempted_students)*100
		failed_percentage =float(100-pass_percentage)
		return (pass_percentage,failed_percentage)
		
		
	def get_dict_values(self):
		return {
		'means':self.marks_sheet.mean(),
		'maximum':self.marks_sheet.max(),
		'minimum':self.marks_sheet.min(),
		'course_marks':self.marks_sheet.sum(),
		}
		
	def get_rows_as_list(self):
		return self.marks_sheet.values
		
	
		
		
			
	def check_fit_model(self):
		try:
			self.set_bar()
			return True
		except:
			return False
			
	def set_pie(self):
		fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
		
		data = self.rows
		ingredients = self.columns
		def func(pct,allvals):
		    absolute = int(pct/100.*np.sum(allvals))
		    return "{:.1f}%\n({:d} g)".format(pct, absolute)

		pct = 'pct'
		wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),textprops=dict(color="w"))
		ax.legend(wedges, ingredients,
          title="Standards",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))
		plt.setp(autotexts, size=8, weight="bold")
		ax.set_title("STANDARD STRENGTH AS PIE")
		plt.savefig(self.animation_pie_file)


animation = FitModel()
