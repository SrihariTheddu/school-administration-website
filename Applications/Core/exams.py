
from Applications.Examination.models import Question,CourseQuestions
from DataProcessorSystem.FixturesInstallation.questions import QUESTIONS



def ParseQuestions(course,QUESTIONS):
	this_questions = []
	for index,question in enumerate(QUESTIONS):
		
		question['question_code']=course.course_code+str(course.standard.standard)+str(index)
		cq_question = Question.objects.create(
is_script=question['is_script'],
is_blank=question['is_blank'],
is_choice=question['is_choice'],
question=question['question'],
question_code=question['question_code'],
option1=question['option1'],
option2=question['option2'],
option3=question['option3'],
option4=question['option4'],
answer=question['answer'],
marks=question['marks']
		)
		this_questions.append(cq_question)
	return this_questions
		
		

def ParseCourseQuestions(course,QUESTIONS):
	cq = CourseQuestions(
	course=course
	)
	cq.save()
	for question in QUESTIONS:
		cq.questions.add(question)
	cq.save()
	
		