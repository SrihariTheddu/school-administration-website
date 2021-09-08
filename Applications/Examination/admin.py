from django.contrib import admin

from mysite.coresettings.appconf import (Examination)

from Applications.Examination.models import (
       Question,
       CourseQuestions,
       TestQuestionPaper,
       TestAnswerSheet,
       CourseResult,
       FinalResult
       )

if Examination.db_read or Examination.db_read:
	
	admin.site.register(Question)
	admin.site.register(CourseQuestions)
	admin.site.register(TestQuestionPaper)
	admin.site.register(TestAnswerSheet)
	admin.site.register(CourseResult)
	admin.site.register(FinalResult)





