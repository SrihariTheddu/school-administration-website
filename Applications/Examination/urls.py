from django.urls import path

from Applications.Examination.views import (
#Student related views..
TestAnswerSheetListView,
PendingTestAnswerSheetListView,
SubmittedTestAnswerSheetListView,
CourseTestAnswerSheetListView,
DraftedAnswerSheetView,
TestQuestionPaperView,
TestAnswerSheetDetailView,
AddAnswerSheetToDraftView,
RemoveAnswerSheetFromDraftView,



#Take Test Instabce
QuestionView,
TestReviewView,
TestSubmitView,
TestResultView,
validate,

#student result page
StudentResultView,
StudentExamResultView,
ResultLoginView,


#staff related views..
PostTestPaperCreateView,
PostedTestDeleteView,
StaffPostedTestListView,
StaffPostedTestDetailView, StaffSubmittedAnswerSheetsListView,
StaffPostCourseQuestionView,
StaffCourseQuestionsListView,
StaffCourseQuestionsDetailView,
StaffCourseQuestionsDeleteView,
StaffQuestionDeleteView,

)

app_name = 'Exams'

urlpatterns = [


#student relatwd views....
path('Exams/tests/all/',TestAnswerSheetListView.as_view(),name='TestAnswerSheet-ListView'),

path('Exams/tests/<str:course_name>/',CourseTestAnswerSheetListView,name='CourseTestAnswerSheetListPage'),

path('Exams/tests/pending/all/',PendingTestAnswerSheetListView.as_view(),name='PendingTestAnswerSheetListPage'),

path('Exams/tests/drafts/all/',DraftedAnswerSheetView.as_view(),name='DraftedAnswerSheetsPage'),

path('Exams/tests/submitted/all/',SubmittedTestAnswerSheetListView.as_view(),name='SubmittedTestAnswerSheetListPage'),

path('Exams/tests/<int:pk>/details/',TestAnswerSheetDetailView.as_view(),name='TestAnswerSheet-DetailView'),

path('Exams/tests/paper/<slug:pk>/',TestQuestionPaperView.as_view(),name='TestQuestionPaper-DetailView'),

path('Exams/tests/<int:pk>/draft/add/',AddAnswerSheetToDraftView,name='AddAnswerSheetToDraftPage'),

path('Exams/tests/<int:pk>/draft/remove/',RemoveAnswerSheetFromDraftView,name='RemoveAnswerSheetFromDraftPage'),


#Take Test Related Views....
path('Exams/tests/paper/question/<slug:pk>/',QuestionView.as_view(),name='Question-DetailView'),

path('Exams/tests/paper/question/<slug:pk>/validate/',validate,name='validate'),

path('Exams/tests/paper/<slug:pk>/review/',TestReviewView.as_view(),name='TestReviewPage'),

path('Exams/tests/paper/<slug:pk>/submit/',TestSubmitView,name='TestSubmitPage'),

path('Exams/tests/paper/<int:pk>/result/',TestResultView.as_view(),name='TestResultPage'),


#Management related views...
path('Exams/result/<int:pk>/',StudentResultView.as_view(),name='StudentResultPage'),

path('Exams/results/<int:pk>/',StudentExamResultView.as_view(),name='StudentExamResultPage'),

path('Exams/result/login/',ResultLoginView.as_view(),
name='ResultLoginPage'),

#Staff Related views....
path('Exams/staff/course/testpaper/add/',PostTestPaperCreateView.as_view(),name='StaffPostTestCreatePage'),

path('staff/tests/<int:pk>/delete/',PostedTestDeleteView,name='PostedTestDeletePage'),

path('staff/tests/<slug:pk>/details/',StaffPostedTestDetailView.as_view(),name='StaffPostedTestDetailPage'),

path('staff/<int:pk>/tests/',StaffPostedTestListView.as_view(),name='StaffPostedTestListPage'),

path('Exams/staff/course/testpaper/<slug:pk>/submissions/',StaffSubmittedAnswerSheetsListView.as_view(),name='StaffSubmittedAnswerSheetListPage'),

path('Exams/staff/course/testpaper/coursequestions/add/',StaffPostCourseQuestionView.as_view(),name='StaffPostCourseQuestionsPage'),

path('staff/course/<int:pk>/cqs/all/',StaffCourseQuestionsListView.as_view(),name='StaffCourseQuestionsListPage'),

path('staff/course/cq/<int:pk>/details',StaffCourseQuestionsDetailView.as_view(),name='StaffCourseQuestionsDetailPage'),

path('staff/course/cq/<int:pk>/delete/',StaffCourseQuestionsDeleteView,name='StaffCourseQuestionsDeletePage'),


path('staff/cqs/questions/<slug:pk>/delete/',StaffQuestionDeleteView,name='StaffQuestionDeleteView'),


]
