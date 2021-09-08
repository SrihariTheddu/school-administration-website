from django.urls import path

from Applications.Main.views import (
    #signing views.....
    SignInView,
    SignOutView,
    
    
    HomePageView,
    IndexPageView,
    LoginPageView,
    LogOutView,
    PasswordChangeView,
    
    #StaffRelated Views...
    StaffIndexPageView,
    StandardStudentListView,
    
    #leaveletters related views
    ApplyLeaveFormView,
    LeaveLetterListView,
    GrantLeaveLetterListView,
    DiscardLeaveLetterListView,
    LeaveLetterDetailView,
    GrantLeaveView,
    DiscardLeaveView,
    
    #Home Page Related views...
    HomeAcademicCalendarView,
    HomeDepartmentListView,
    HomeManagementListView,
    HomeStandardListView,
    HomeAccredationPageView,
    HomeAboutPageView,
    )
    
from Applications.Main.install_packages import (
      BasicAdminPanel,
      
)

app_name = 'Main'

urlpatterns = [

path('',BasicAdminPanel.CheckManagerView,name='Constructor'),
path('add/admin/',BasicAdminPanel.AddAdminView,name='AddAdminView'),

path('add/admin/install/transactions/',BasicAdminPanel.install_transactions,name='InstallTransactions'),

#signing views....
path('signin/',SignInView.as_view(),name='SignInPage'),

path('signout/',SignOutView.as_view(),name='SignOutPage'),


#http://127.0.0.1:8000/login/
path('login/',LoginPageView.as_view(),name='LoginPage'),

#http://127.0.0.1:8000/home/
path('home/',HomePageView.as_view(),name='HomePage'),
   
#http://127.0.0.1:8000/hari/index
path('<int:pk>/index/',IndexPageView.as_view(),name='IndexPage'),

path('changepassword/',PasswordChangeView.as_view(),name='ChangePasswordPage'),

path('logout/',LogOutView.as_view(),name='LogOutPage'),

#staff related views.....
path('<int:pk>/staffindex/',StaffIndexPageView.as_view(),name='StaffIndexPage'),

path('staff/standard/<int:pk>/students/all/',StandardStudentListView.as_view(),name='StandardStudentListPage'),


#Apply Leave Letters related views..
path('apply/leave/',ApplyLeaveFormView.as_view(),name='ApplyLeaveFormPage'),

path('staff/leaveletters/all/',LeaveLetterListView.as_view(),name='LeaveLetterListPage'),

path('staff/leaves/granted/all/',GrantLeaveLetterListView.as_view(),name='GrantLeaveLetterListPage'),

path('staff/leaves/discard/all/',DiscardLeaveLetterListView.as_view(),name='DiscardLeaveLetterListPage'),

path('staff/leave/<int:pk>/details/',LeaveLetterDetailView.as_view(),name='LeaveLetterDetailPage'),

path('staff/leave/<int:pk>/grant/',GrantLeaveView,name='GrantLeavePage'),

path('staff/leave/<int:pk>/discard/',DiscardLeaveView,name='DiscardLeavePage'),


#Home related views.....
path('academic-calender/',HomeAcademicCalendarView.as_view(),name='AcademicCalendarPage'),


path('departments/all/',HomeDepartmentListView.as_view(),name='HomeDepartmentListPage'),

path('standards/all/',HomeStandardListView.as_view(),name='HomeStandardListPage'),

path('Accredation/',HomeAccredationPageView.as_view(),name='HomeAccredationPage'),

path('aboutpage/',HomeAboutPageView.as_view(),name='HomeAboutPage'),

path('managements/all/',HomeManagementListView.as_view(),
name='HomeManagementListPage')



]