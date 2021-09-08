from django.urls import path

app_name = 'Management'

from Applications.Management.views import (
         EventDetailView,
         EventRegisterFormView,
         EventListView,
         ParticipentsListView,
         EventRegisterView,
         AddEventToDraftView,
         RemoveEventFromDraftView,
         DraftedEventListView
         )



urlpatterns = [

path('Events/',EventListView.as_view(),name='EventListPage'),

path('Events/<int:pk>/details/',EventDetailView.as_view(),name='EventDetailPage'),

path('Events/drafts/all/',DraftedEventListView.as_view(),name='DraftedEventListPage'),

path('Events/<int:pk>/members/',ParticipentsListView.as_view(),name='EventListPage'),

path('Events/<int:pk>/registerform/',EventRegisterFormView.as_view(),name='EventRegisterFormPage'),

path('Events/<int:pk>/registerform/register/',EventRegisterView,name='EventRegisterPage'),

path('Events/<int:pk>/draft/add/',AddEventToDraftView,name='AddDraftEventPage'),

path('Events/<int:pk>/draft/add/',RemoveEventFromDraftView,name='RemoveDraftEventPage')
]

