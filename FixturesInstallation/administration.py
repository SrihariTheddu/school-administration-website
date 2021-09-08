from Applications.Administration.models import (Channel,Standard)

students = [
   {
   'username':'student11',
   'standard':Standard.objects.get_or_create(standard=1)[0],
   },
   
   {
   'username':'student12',
   'standard':Standard.objects.get_or_create(standard=1)[0]
   },
   
   {
   'username':'student21',
   'standard':Standard.objects.get_or_create(standard=2)[0]
   },
   
   {
   'username':'student22',
   'standard':Standard.objects.get_or_create(standard=2)[0]
   },
   
   {
   'username':'student31',
   'standard':Standard.objects.get_or_create(standard=3)[0]
   },
   
   {
   'username':'student32',
   'standard':Standard.objects.get_or_create(standard=3)[0]
   },
]

managers = [

   {
   'username':'PT_SIR',
   'standard':Standard.objects.get_or_create(standard=0)[0]
   },
   
   {
   'username':'ManagementHead',
   'standard':Standard.objects.get_or_create(standard=0)[0]
   },
   
   {
   'username':'AdministrationHead',
   'standard':Standard.objects.get_or_create(standard=0)[0]
   },
   
   {
   'username':'FeeCounterHead',
   'standard':Standard.objects.get_or_create(standard=0)[0]
   },
   
   {
   'username':'ExamHead',
   'standard':Standard.objects.get_or_create(standard=0)[0]
   }
   
   
]


staff = [
   
   {
   'username':'staff1',
   'standard':1,
   },
   
   {
   'username':'staff2',
   'standard':2,
   },
   
   {
   'username':'staff3',
   'standard':3
   },
   
]

standards =[ 

     {
       'standard':1,
    	},
    	
    {
        'standard':2
    },
    
    {
    'standard':3
    }
    
]


departments = [

    {
  'head':Channel.objects.get_or_create(username='AdministrationHead')[0],
  'title':'Administration',
  'vision':'TO PROCESS THE ADMISSION PROCESS OF THE STUDENTS SUCCESSFULLY',
  'message':'WELCOME TO NEW ACADEMICS',
 },
 
  {
   'head':Channel.objects.get_or_create(username='ExamHead')[0],
  'title':'Examination',
  'vision':'TO CONDUCT EXAMS IN AN APPROPRIATE FORMAT BY GUIDELINES PROVIDED BY THE HEAD OF THE MANAGEMENT',
  'message':'ALL THE BEST'
 },
 
 {
  'head':Channel.objects.get_or_create(username='FeeCounterHead')[0],
  'title':'Fee Counter',
  'vision':'TO PROCESS THE FINANICAL SYSTEM OF THE INSTITUTION',
  'message':'PAY THE FEES PROMPTLY TO AVOID INCONVIENCE FROM THE MANAGEMENT'
 }

]






