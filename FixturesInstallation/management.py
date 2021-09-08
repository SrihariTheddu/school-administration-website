
from Applications.Management.models import Management
from Applications.Administration.models import Channel


managements = {
  
  'management1':{
  'name':'INDEPENDENCE DAY',
  'head':Channel.objects.get(username='PT_SIR')
  },
  
  'management2':{
  'name':'REPUBLIC DAY',
  'head':Channel.objects.get(username='PT_SIR'),
  },
  
  'management3':{
  'name':'ANNUAL DAY',
  'head':Channel.objects.get(username='PT_SIR')
  },
  
   'management4':{
  'name':'FRESHERS DAY',
  'head':Channel.objects.get(username='PT_SIR')
  }


}

events = {
  
  'event1':{
  'event':'FRESHERS DAY',
  'vision':'TO CONDUCT THE FRESHIERS DAY.....',
  'management':Management.objects.get_or_create(name='Management')[0]
  }

}

