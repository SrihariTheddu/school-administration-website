from django.urls import path

app_name = 'Admin'



from Applications.Administration.views import (

#profile related views
ProfilePageView,
ApplyTCView,
ChangeMobileNumberView,
FeedBackView,
AppointmentFormView,

#Admissions related views
AdmissionFormView,
ApplicationStatusView,
SearchApplicationView,


#Manager related views
ManagerBlogView,

#admissions
ManagerAdmissionListView,
ManagerAdmissionDetailView,
ManagerApproveAdmissionView,
ManagerDiscardAdmissionView,
ManagerApproveAdmissionListView,
ManagerDiscardAdmissionListView,
ManagerAdmissionDeleteView,

#Course Related...
ManagerCourseCreateView,
ManagerCourseListView,
ManagerCourseDetailView,
ManagerCourseDeleteView,

#Standard related ....
ManagerStandardCreateView,
ManagerStandardListView,
ManagerStandardDeleteView,
ManagerStandardDetailView,

#Staff related viewss..
ManagerStaffCreateView,
ManagerStaffListView,
ManagerStaffDetailView,
ManagerStaffDeleteView,
ManagerStaffEditView,
StaffProfileView,

#Student related viewss..
ManagerChannelCreateView,
ManagerChannelListView,

#Manager Events....
ManagerEventCreateView,
ManagerEventListView,
ManagerEventDeleteView,
ManagerEventDetailView,

#circular related views...
ManagerCircularCreateView,
ManagerCircularListView,
ManagerCircularDeleteView,
ManagerCircularDetailView,

#Management related?....
ManagerManagementCreateView,
ManagerManagementListView,
ManagerManagementDetailView,
ManagerManagementDeleteView,
ManagerManagementChangeHeadView,
ManagerManagementAddMemberView,
ManagerManagementRemoveMemberView,


#Departmentment related?....
ManagerDepartmentCreateView,
ManagerDepartmentListView,
ManagerDepartmentDetailView,
ManagerDepartmentDeleteView,
ManagerDepartmentEditView,
ManagerDepartmentChangeHeadView,
ManagerDepartmentAddMemberView,
ManagerDepartmentRemoveMemberView,

ManagerPostFeeReminderView,
ManagerFeeReminderListView,
ManagerChangeNumberListView,
ManagerResultAnimationView,


ManagerTCFormListView,
ManagerTCFormDetailView,
ManagerTCFormApproveView,
ManagerTCFormDiscardView,
ManagerTCFormDeleteView,
ManagerTCFormApproveListView,
ManagerTCFormDiscardListView,

ManagerAppointmentListView,
ManagerAppointmentDetailView,
ManagerAppointmentApproveView,
ManagerAppointmentDiscardView,
ManagerAppointmentDeleteView,
ManagerApproveAppointmentListView,
ManagerDiscardAppointmentListView,

#ExtraFunctions
StandardListView,
StandardDetailView,

ManagerFeedBackListView,
ManagerDraftedFeedBackListView,
ManagerFeedBackReplyView,  
ManagerAddFeedBackToDraftView, 
ManagerRemoveFeedBackFromDraftView, 
ManagerFeedBackDeleteView,
         
               )
               
urlpatterns = [

#profile related views....
path('student/<int:pk>/details/',ProfilePageView.as_view(),name='ProfilePage'),

path('applytc/',ApplyTCView.as_view(),
name='ApplyTCFormPage'),

path('change/mobile-number/',ChangeMobileNumberView.as_view(),name='ChangeMobileNumberPage'),

path('student/feedback/',FeedBackView.as_view(),name='FeedBackPage'),

path('student/appointment/',AppointmentFormView.as_view(),name='AppointmentFormPage'),

#Admissions Related views....
path('apply/form/',AdmissionFormView.as_view(),
name='ApplicationFormPage'),

path('staff/admissions/all',ManagerAdmissionListView.as_view(),name='ManagerAdmissionListPage'),

path('manager/admission/<int:pk>/details/',ManagerAdmissionDetailView.as_view(),name='ManagerAdmissionDetailPage'),

path('staff/admissions/approve/all',ManagerApproveAdmissionListView.as_view(),name='ManagerApproveAdmissionListPage'),

path('staff/admissions/discard/all',ManagerDiscardAdmissionListView.as_view(),name='ManagerDiscardAdmissionListPage'),


path('applications/search/',SearchApplicationView.as_view(),name='ApplicationSearchPage'),

path('application/<int:pk>/status/',ApplicationStatusView.as_view(),name='ApplicationStatusPage'),

path('manager/admission/<int:pk>/approve/',ManagerApproveAdmissionView,name='ManagerApproveAdmissionPage'),

path('manager/admission/<int:pk>/discard/',ManagerDiscardAdmissionView,name='ManagerDiscardAdmissionPage'),

path('manager/admission/<int:pk>/delete/',ManagerAdmissionDeleteView.as_view(),name='ManagerAdmissionDeletePage'),

#Manager related views....
path('home/managers/blog/',ManagerBlogView.as_view(),name='ManagerBlogPage'),

#Manager StaffRelated Views
path('manager/staffs/add/',ManagerStaffCreateView.as_view(),name='ManagerStaffCreatePage'),

path('manager/staffs/all/',ManagerStaffListView.as_view(),name='ManagerStaffListPage'),

path('manager/staffs/<int:pk>/details/',ManagerStaffDetailView.as_view(),name='ManagerStaffDetailPage'),

path('manager/staffs/<int:pk>/delete/',ManagerStaffDeleteView,name='ManagerStaffDeletePage'),

path('manager/staffs/<int:pk>/profile/',StaffProfileView.as_view(),name='StaffProfilePage'),

#Manager Student Admissions
path('manager/channels/add/',ManagerChannelCreateView.as_view(),name='ManagerChannelCreatePage'), 

path('manager/channels/all/',ManagerChannelListView.as_view(),name='ManagerChannelListPage'),
  
#Manager Course related....
path('manager/courses/add/',ManagerCourseCreateView.as_view(),name='ManagerCourseCreatePage'),  
  
path('manager/courses/all/',ManagerCourseListView.as_view(),name='ManagerCourseListPage'),

path('manager/course/<int:pk>/details/',ManagerCourseDetailView.as_view(),name='ManagerCourseDetailPage'), 
  
path('manager/course/<int:pk>/delete/',ManagerCourseDeleteView,name='ManagerCourseDeletePage'),  
  
#Manager Standard related....
path('manager/standards/add/',ManagerStandardCreateView.as_view(),name='ManagerStandardCreatePage'),  
  
path('manager/standards/all/',ManagerStandardListView.as_view(),name='ManagerStandardListPage'),

path('manager/standards/<int:pk>/details/',ManagerStandardDetailView.as_view(),name='ManagerStandardDetailPage'), 
  
path('manager/standard/<int:pk>/delete/',ManagerStandardDeleteView,name='ManagerStandardDeletePage'),  
  
  
#Manager Events related....
path('manager/events/add/',ManagerEventCreateView.as_view(),name='ManagerEventCreatePage'),  
  
path('manager/events/all/',ManagerEventListView.as_view(),name='ManagerEventListPage'),

path('manager/events/<int:pk>/details/',ManagerEventDetailView.as_view(),name='ManagerEventDetailPage'), 
  
path('manager/events/<int:pk>/delete/',ManagerEventDeleteView,name='ManagerEventDeletePage'),  
 
#Manager Circular related.... 
path('manager/circulars/create/',ManagerCircularCreateView.as_view(),name='ManagerCircularCreatePage'),

path('manager/circulars/all/',ManagerCircularListView.as_view(),name='ManagerCircularListPage'),

path('manager/circulars/<int:pk>/details/',ManagerCircularDetailView.as_view(),name='ManagerCircularDetailPage'), 

path('manager/circulars/<int:pk>/delete/',ManagerCircularDeleteView,name='ManagerCircularDeletePage'),

#Manager related management
path('manager/managements/create/',ManagerManagementCreateView.as_view(),name='ManagerManagementCreatePage'),

path('manager/managements/all/',ManagerManagementListView.as_view(),name='ManagerManagementListPage'),

path('manager/managements/<int:pk>/details/',ManagerManagementDetailView.as_view(),name='ManagerManagementDetailPage'),

path('manager/managements/<int:pk>/delete/',ManagerManagementDeleteView,name='ManagerManagementDeletePage'),

path('manager/managements/<int:pk>/head/',ManagerManagementChangeHeadView.as_view(),name='ManagerManagementChangeHeadPage'),

path('manager/managements/<int:pk>/edit/head/change/',ManagerManagementChangeHeadView.change_head,name='ManagerManagementChangeHeadView'),

path('manager/managements/<int:pk>/edit/memerspage/',ManagerManagementAddMemberView.as_view(),name='ManagerManagementAddMemberPage'),

path('manager/managements/<int:pk>/edit/memers/add/',ManagerManagementAddMemberView.add_member,name='ManagerManagementAddMemberView'),

path('manager/managements/<int:management>/edit/members/<int:pk>/remove/',ManagerManagementRemoveMemberView,name='ManagerManagementRemoveMemberView'),

#Manager related Department
path('manager/departments/create/',ManagerDepartmentCreateView.as_view(),name='ManagerDepartmentCreatePage'),

path('manager/departments/all/',ManagerDepartmentListView.as_view(),name='ManagerDepartmentListPage'),

path('manager/departments/<int:pk>/details/',ManagerDepartmentDetailView.as_view(),name='ManagerDepartmentDetailPage'),

path('manager/departments/<int:pk>/delete/',ManagerDepartmentDeleteView,name='ManagerDepartmentDeletePage'),

path('manager/departments/<int:pk>/head/',ManagerDepartmentChangeHeadView.as_view(),name='ManagerDepartmentChangeHeadPage'),

path('manager/departments/<int:pk>/edit/head/change/',ManagerDepartmentChangeHeadView.change_head,name='ManagerDepartmentChangeHeadView'),

path('manager/departments/<int:pk>/edit/memerspage/',ManagerDepartmentAddMemberView.as_view(),name='ManagerDepartmentAddMemberPage'),

path('manager/departments/<int:pk>/edit/memers/add/',ManagerDepartmentAddMemberView.add_member,name='ManagerDepartmentAddMemberView'),

path('manager/departments/<int:department>/edit/members/<int:pk>/remove/',ManagerDepartmentRemoveMemberView,name='ManagerDepartmentRemoveMemberView'),

path('manager/fee_reminder/<int:pk>/post/',ManagerPostFeeReminderView,name='ManagerPostFeeReminderPage'),

path('manager/fee_reminders/all/',ManagerFeeReminderListView.as_view(),name='ManagerFeeReminderListPage'),



path('manager/mobile_numbers/change/all/',ManagerChangeNumberListView.as_view(),name='ManagerChangeNumberListPage'),


 
#Common views
path('manager/standard/all/',StandardListView.as_view(),name='HomeStandardListPage'),
 
path('manager/standard/<int:pk>/details/',StandardDetailView.as_view(),name='StandardDetailPage'),

path('manager/results/animations/<int:pk>/',ManagerResultAnimationView.as_view(),name='ManagerResultAnimationPage'),


path('manager/tcforms/all/',ManagerTCFormListView.as_view(),name='ManagerTCFormListPage'),

path('manager/tcforms/<int:pk>/view/',ManagerTCFormDetailView.as_view(),name='ManagerTCFormDetailPage'),

path('manager/tcforms/<int:pk>/approve/',ManagerTCFormApproveView,
name='ManagerTCFormApprovePage'),

path("manager/tvforms/<int:pk>/discard/",ManagerTCFormDiscardView,name='ManagerTCFormDiscardPage'),

path("manager/tvforms/<int:pk>/delete/",ManagerTCFormDeleteView,name='ManagerTCFormDeletePage'),

path('manager/tcforms/discard/all/',ManagerTCFormDiscardListView.as_view(),name='ManagerTCFormDiscardListPage'),

path('manager/tcforms/approve/all/',ManagerTCFormApproveListView.as_view(),name='ManagerTCFormApproveListPage'),

path('manager/appointments/all/',ManagerAppointmentListView.as_view(),name='ManagerAppointmentListPage'),

path('manager/appointments/<int:pk>/view/',ManagerAppointmentDetailView.as_view(),name='ManagerAppointmentDetailPage'),

path('manager/appointments/<int:pk>/approve/',ManagerAppointmentApproveView,
name='ManagerAppointmentApprovePage'),

path("manager/appointments/<int:pk>/discard/",ManagerAppointmentDiscardView,name='ManagerAppointmentDiscardPage'),

path("manager/appointments/<int:pk>/delete/",ManagerAppointmentDeleteView,name='ManagerAppointmentDeletePage'),

path('manager/appointments/discard/all/',ManagerDiscardAppointmentListView.as_view(),name='ManagerDiscardAppointmentListPage'),

path('manager/appointments/approve/all/',ManagerApproveAppointmentListView.as_view(),name='ManagerApproveAppointmentListPage'),


path("manager/feedbacks/all/",ManagerFeedBackListView.as_view(),name='ManagerFeedBackListPage'),

path("manager/feedbacks/drafts/",ManagerDraftedFeedBackListView.as_view(),name='ManagerDraftedFeedBackListPage'),

path("manager/feedback/<int:pk>/reply",ManagerFeedBackReplyView.as_view(),name='ManagerFeedBackReplyPage'),



path('manager/feedback/<int:pk>/draft/',ManagerAddFeedBackToDraftView,name='ManagerAddFeedBackToDraftPage'),

path('manager/feedback/<int:pk>/remove/',ManagerRemoveFeedBackFromDraftView,name='ManagerRemoveFeedBackFromDraftPage'),

path('manager/feedback/<int:pk>/delete/',ManagerFeedBackDeleteView,name='ManagerFeedBackDeletePage')

 ]