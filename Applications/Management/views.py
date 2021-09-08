from django.shortcuts import (
        render,
        redirect
        )

from Applications.DashBoard.models import (
          Notification,
          Circular,
          Reminder)
from Applications.Administration.models import (
               Channel,
               Standard)
          
from Applications.Management.models import (
          EventRegister,
          Event,
          Management,
          SchoolTeam,
          Player
          )

from django.views.generic import (
           CreateView,
           DeleteView,
           DetailView,
           UpdateView,
           ListView,
           TemplateView,
           )
           
from django.core.cache import cache

from django.contrib import messages

from Applications.Core.loader import CacheLoader



def check_event_in_draft(channelcontent,event,flag=False):
    for event_form in channelcontent.events.all():
        if event_form==event:
            flag=True
            break
    return flag


#Event related objects.....
class EventListView(ListView,CacheLoader):
	model = Event
	context_object_name = 'events'
	
	def get_template_names(self):
	    channel = cache.get('channel')
	    if channel.is_staff:
	        return 'StaffBlogPage.html'
	    elif channel.is_manager:
	        return 'ManagerBlogPage.html'
	    else:
	        return 'ProfileLayerPage.html'
	        
	def get_context_data(self,**kwargs):
	    kwargs = self.load_cache(kwargs)
	    kwargs['channelcontent']=cache.get('channelcontent')
	    kwargs['title']='EVENTS'
	    kwargs['drafts']=False
	    kwargs['template']='EventListPage.html'
	    kwargs['main_template']='EventListPage.html'
	    
	    return super().get_context_data(**kwargs)
	    

class DraftedEventListView(ListView,CacheLoader):
	model = Event
	template_name = 'EventListPage.html'
	context_object_name = 'events'
	
	def get_queryset(self):
	    return cache.get('channelcontent').events.all()
	
	def get_context_data(self,**kwargs):
	    kwargs = self.load_cache(kwargs)
	    kwargs['title']='DRAFTS'
	    kwargs['drafts']=True
	    return super().get_context_data(**kwargs)
	
class EventDetailView(DetailView,CacheLoader):
	model = Event
	template_name = 'EventDetailPage.html'
	context_object_name = 'event'
	
	def get_context_data(self,**kwargs):
	    kwargs = self.load_cache(kwargs)
	    kwargs['is_drafted']=check_event_in_draft(cache.get('channelcontent'),self.object)
	    print(kwargs['is_drafted'])
	    
	    return super().get_context_data(**kwargs)

class EventRegisterFormView(DetailView,CacheLoader):
	model = Event
	template_name = 'EventRegisterPage.html'
	context_object_name = 'event'
	
	
	def get_context_data(self,**kwargs):
	    kwargs = self.load_cache(kwargs)
	    return super().get_context_data(**kwargs)
	    
	    
	
def EventRegisterView(request,pk):
    username = request.GET['username']
    standard = Standard.objects.get(standard=int(request.GET['standard']))
    adm_num = int(request.GET['adm_num'])
    event = Event.objects.get(pk=pk)
    event_form = EventRegister(
    username=username,
    standard=standard,
    admission_number = adm_num)
    event_form.save()
    event.participents.add(event_form)
    return redirect('Management:EventListPage')
    
    def get_context_data(self,**kwargs):
	    kwargs = self.load_cache(kwargs)
	    return super().get_context_data(**kwargs)
	
def AddEventToDraftView(request,pk):
    event=Event.objects.get(pk=pk)
    channelcontent = cache.get('channelcontent')
    channelcontent.events.add(event)
    cache.set('channelcontent',channelcontent)
    return redirect('Management:DraftedEventListPage')

def RemoveEventFromDraftView(request,pk):
    event=Event.objects.filter(pk=pk)
    channelcontent = cache.get('channelcontent')
    channelcontent.events.remove(event)
    cache.set('channelcontent',channelcontent)
    return redirect('Management:DraftedEventListPage')
	
class ParticipentsListView(DetailView,CacheLoader):
	model = Event
	template_name = 'ParticipentsListPage.html'
	
	def get_context_data(self,**kwargs):
	    kwargs = self.load_cache(kwargs)
	    return super().get_context_data(**kwargs)
	    
	    
#schòol sports relayed views..
class SchoolTeamView(DetailView,CacheLoader):
    model = SchoolTeam
    template_name = 'SchoolTeamPage.html'
    
    def get_context_data(self,**kwargs):
        kwargs = self.load_cache(kwargs)
        return super().get_context_data(**kwargs)
        

