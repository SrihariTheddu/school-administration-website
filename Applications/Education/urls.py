from django.urls import path
from Applications.Education.views import (

#HomeRelatedViewa.......
AllCoursesView,
StandardCoursesListView,


#Students related views...

#courses
CourseListView,
CourseDetailView,
ExCourseDetailView,
RegisterCourseView,
SearchCourseView,

#course contents...
ContentPDFView,
UnitPDFView,
DownloadUnitPDFView,


#Student Assignments
AssignmentListView,
SubmittedAssignmentsListView,
PendingAssignmentsListView,
DraftedAssignmentsView,
AssignmentDetailView,
submit_assignment,
UpdateAssignmentView,
AddAssignmentToDraftView,
RemoveAssignmentFromDraftView,


#staff relted views...

#courses relates
StaffCoursesListView,
StaffCourseDetailView,

#Assignments related...
PostAssignmentCreateView,
CourseAssignmentsListView,
StaffSubmittedAssignmentListView,
PostedAssignmentListView,
PostedAssignmentDetailView,
PostedAssignmentDeleteView,

#Tutorial related...
StaffPostTutorialCreateView,
StaffPostedTutorialListView,
StaffPostedTutorialDetailView,
StaffPostedTutorialDeleteView,

StaffAddUnitToContentView,
StaffRemoveUnitFormContentView,
StaffCourseContentDetailView,
StaffCourseContentCreateView,



#Extra
PostedTestListView,

)

app_name = 'Education'

urlpatterns = [

#Home relates....
path('courses/all/',AllCoursesView.as_view(),name='AllCoursesPage'),

path('courses/standard<int:pk>/',StandardCoursesListView.as_view(),name='StandardCoursesListPage'),


#Student related views...


#courses related.....
path('courses/',CourseListView.as_view(),name='CourseListPage'),

path('courses/<int:pk>/details/',CourseDetailView.as_view(),name='CourseDetailPage'),

path('courses/<int:pk>/ex/',ExCourseDetailView.as_view(),name='ExCourseDetailPage'),

path('courses/<int:pk>/register/',RegisterCourseView.as_view(),name='RegisterCoursePage'),

path('allcourses/search/',SearchCourseView,name='SearchCourse'),


#assignments relates....
path('assignments/',AssignmentListView.as_view(),
name='AssignmentListPage'),

path('assignments/<str:course_name>/all/',CourseAssignmentsListView,
name='CourseAssignmentsListPage'),

path('assignment/draft/all/',DraftedAssignmentsView.as_view(),name='DraftedAssignmentsPage'),

path('assignment/<int:pk>/',AssignmentDetailView.as_view(),
name='AssignmentDetailPage'),

path('assignment/submit/',submit_assignment,name='SubmitAssignmentPage'),

path('assignment/<int:pk>/edit/',UpdateAssignmentView.as_view(),name='EditAssignmentPage'),

path('assignment/<int:pk>/draft/add/',AddAssignmentToDraftView,name='AddAssignmentToDraftPage'),

path('assignment/<int:pk>/draft/remove/',RemoveAssignmentFromDraftView,name='RemoveAssignmentFromDraftPage'),
path('courses/student/assignments/submissons/',SubmittedAssignmentsListView.as_view(),name='SubmittedAssignmentsListPage'),

path('courses/student/assignments/Pending/',PendingAssignmentsListView.as_view(),name='PendingAssignmentsListPage'),



#course content relates...
path('courses/content/<int:pk>/',ContentPDFView.as_view(),name='ContentPDFPage'),

path('courses/unit/<slug:pk>/',UnitPDFView.as_view(),name='UnitPDFPage'),

path('courses/unit/download/<slug:pk>/',DownloadUnitPDFView.as_view(),name='DownloadUnitPDFPage'),




#staff related views..

#course related

path('courses/staff/',StaffCoursesListView.as_view(),name='StaffCoursesListPage'),

path('courses/staff/<int:pk>/index/',StaffCourseDetailView.as_view(),name='StaffCourseDetailPage'),


#Assignments related...

path('staff/assignments/post/',PostAssignmentCreateView.as_view(),name='PostAssignmentCreatePage'),


path('courses/assignments/<int:pk>/submissons/',StaffSubmittedAssignmentListView.as_view(),name='StaffSubmittedAssignmentListPage'),



path('staff/assignments/<int:pk>/posted/all/',PostedAssignmentListView.as_view(),name='StaffPostedAssignmentListPage'),

path('staff/assignments/posts/<int:pk>/details/',PostedAssignmentDetailView.as_view(),name='PostedAssignmentDetailPage'),

path('staff/assignments/posts/<int:pk>/delete/',PostedAssignmentDeleteView,name='PostedAssignmentDeletePage'),




#Tutorilas related..
path('staff/tutorials/post/',StaffPostTutorialCreateView.as_view(),name='StaffPostTutorialCreatePage'),

path('staff/<int:pk>/tutorials/all/',StaffPostedTutorialListView.as_view(),name='StaffPostedTutorialListPage'),

path('staff/<int:pk>/tutorials/details/',StaffPostedTutorialDetailView.as_view(),name='StaffPostedTutorialDetailPage'),

path('staff/tutorials/<int:pk>/delete/',StaffPostedTutorialDeleteView,name='StaffPostedTutorialDeletePage'),

path('staff/course/<int:pk>/content/view/',StaffCourseContentDetailView.as_view(),name='StaffCourseContentDetailPage'),
path('staff/course/content/add/',StaffAddUnitToContentView.as_view(),name='StaffAddUnitToCourseContentPage'),

path('staff/course/<slug:pk>/content/units/add/',StaffRemoveUnitFormContentView,name='StaffRemoveUnitFormContentPage'),


path('staff/course/<slug:pk>/content/add/',StaffCourseContentCreateView,name='StaffCourseContentCreatePage')

]
