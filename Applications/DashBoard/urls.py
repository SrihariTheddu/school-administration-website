from django.urls import path

app_name = 'DashBoard'

from Applications.DashBoard.views import (

#student related viewz...
InBoxView,
DraftContextBoxView,
NotificationListView,
ReminderListView,
CircularListView,
ContextDetailView,
DeleteContextView,
ReplyContextView,
ClearAllView,
AddDraftContextView,
RemoveDraftContextView,

#Group Chat related views..
GroupChatView,
PostChatView,
GroupMembersView,
GroupMediaView,
MyChatsView,
         
         
#StaffRelated views

#reminders
StaffReminderCreateView,
StaffReminderListView,
         
#notifications  
StaffNotificationCreateView,
StaffNotificationListView,

#all
StaffContextDetailView,
StaffContextDeleteView,
         
               )
               
urlpatterns = [

#students related..
path('contexts/all/',InBoxView.as_view(),name='InBoxPage'),

path('contexts/drafts/all/',DraftContextBoxView.as_view(),name='DraftContextBoxPage'), 
  
path('notifications/all/',NotificationListView.as_view(),name='NotificationListPage'),
  
path('reminders/all/',ReminderListView.as_view(),name='ReminderListPage'),
  
path('circulars/all/',CircularListView.as_view(),name='CircularListPage'),
  
path('contexts/<slug:code>/',ContextDetailView,name='ContextDetailPage'),
  
path('contexts/all/clear/',ClearAllView,name='ClearAllPage'),
  
path('contexts/<slug:code>/delete/',DeleteContextView,name='DeleteContextPage'),
  
path('contexts/<slug:code>/draft/add/',AddDraftContextView,name='AddDraftContextPage'),
  
path('contexts/<slug:code>/draft/remove',RemoveDraftContextView,name='RemoveDraftContextPage'),
  
path('contexts/<slug:code>/reply/',ReplyContextView,name='ReplyContextPage'),

#Group Chat related views ..  
path('groupchat/<int:pk>/',GroupChatView.as_view(),name='GroupChatPage'),
  
path('groupchat/<int:pk>/post/',PostChatView,name='PostChatPage'),
  
path('groupchat/<int:pk>/members/all/',GroupMembersView.as_view(),name='GroupMembersPage'),
   
path('groupchat/<int:pk>/media/all/',GroupMediaView.as_view(),name='GroupMediaPage'),


path('groupchat/mychats/all/',MyChatsView.as_view(),name='MyChatsPage'),
   
#Staff related urls
path('my-staff/reminders/post/',
StaffReminderCreateView.as_view(),name='StaffReminderCreatePage'),
      
path('my-staff/reminders/all/',StaffReminderListView.as_view(),
name='StaffReminderListPage'),
   
path('my-staff/notifications/post/jsjjsj/hsjjsjsj/',
StaffNotificationCreateView.as_view(),name='StaffNotificationCreatePage'),
      
path('my-staff/notifications/all/',StaffNotificationListView.as_view(),
name='StaffNotificationListPage'),
   
   
path('my-staff/contexts/<slug:code>/details/',StaffContextDetailView,name='StaffContextDetailPage'),
   
path('my-staff/context/<slug:code>/delete/',StaffContextDeleteView,name='StaffContextDeletePage'),
   

]