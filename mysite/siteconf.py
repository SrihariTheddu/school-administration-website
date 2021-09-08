import os
from datetime import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#-----------------------------------
'''
    Include Apps To website  
    if any default occurs in the app
    just shut down the Application 
    simply by modfiying the boolean 
    value to False.
    
    But when you shut down the Main 
    Application the entire website 
    is to be shut down.
    because server runs mainly on 
    this application....
    
    Application Settings.
    
    Install Application:
    -------------------
    It installs the Application 
        the project.
        
        
    Shut Down Application :
    ---------------------
        Completely closes the Application including DataBase.
        
    Stop Application:
    ----------------
        It shut down the application
        but Database runs and can 
        Process
        
    Download Data From Server:
    -------------------------
         It allows Application to 
         download data from database
         
         
    Upload Data To Server:
    ---------------------
         It allows Application to Upload Data To DataBase....
         
    Record Transactions:
    -------------------
         It records the transactions
         of that particular 
         Application
      
    '''

MAIN = {
'App Label':'Main',
'Install Application':True,
'Upload Data To DataBase':True,
'Download Data From DataBase':False,
'Run Application':True,
}

ADMINISTRATION = {
'App Label':'Administration',
'Install Application':True,
'Upload Data To DataBase':True,
'Download Data From DataBase':False,
'Run Application':True,
}


EXAMINATION = {
'App Label':'Examination',
'Install Application':True,
'Upload Data To DataBase':True,
'Download Data From DataBase':True,
'Run Application':True,
}




TRANSACTIONS ={
'App Label':'Transactions',
'Install Application':True,
'Upload Data To DataBase':True,
'Download Data From DataBase':False,
'Run Application':True,
}


EDUCATION ={
'App Label':'Education',
'Install Application':True,
'Upload Data To DataBase':True,
'Download Data From DataBase':False,
'Run Application':True,
}


MANAGEMENT ={
'App Label':'Management',
'Install Application':True,
'Upload Data To DataBase':True,
'Download Data From DataBase':False,
'Run Application':True,
}


DASHBOARD ={
'App Label':'DashBoard',
'Install Application':True,
'Upload Data To DataBase':True,
'Download Data From DataBase':False,
'Run Application':True,
}



#ADMINISTRATION  CONFIGURATIONS
def configure_options(options):
	response = []
	for option in options:
		response.append((option,option))
	return tuple(response)

#Languages configured in the site...
LANGUAGES = [
 'Telugu',
 'Hindi',
 'English'
]
MODEL_LANGUAGES=configure_options(LANGUAGES)

#caste oriented in the site
CASTES = [ 
  'SC',
  'ST',
  'BC-A',
  'BC-B',
  'BC-C'
  'BC-D',
  'BC-E',
  'OC',
  'OBC'

]
MODEL_CASTES=configure_options(CASTES)


SECTIONS = [
   'A','B'
]

MODEL_SECTIONS=configure_options(SECTIONS)

TC_STATUS = [
     'APPLIED',
     'VERIFIED AT EXAMINATION',
     'VERIFIED BY TRANSACTIONS',
     'VERIFIED BY VICE CHANCELLOR'
     'GRANTED'
]

MODEL_TC_STATUS = configure_options(TC_STATUS)

PAYMENT_FORMS = [
 'January',
 'Feburary',
 'March',
 'April',
 'May',
 'June',
 'July',
 'August',
 'september',
 'October',
 'November',
 'December',
 'Admission',
 'Exam',
 'Term1',
 'Term2'
]

MODEL_PAYMENT_FORMS = configure_options(PAYMENT_FORMS)


CONTRACT_VALIDATION=datetime(2021,6,20)

STATUS_OPTIONS=[
    'PRIMARY_TEACHER',
    'SECONDARY_TEACHER',
    'ACCOUNTANT',
    'PRINICIPAL',
    'VICE-PRINCIPAL',
    'MANAGER',
    'STUDENT'
    
]

MODEL_STATUS_OPTIONS = configure_options(STATUS_OPTIONS)

ADMISSION_STATUS_OPTIONS = [
     'APPLIED',
     'VERIFIED',
     'PROCEDING',
     'ADMITTED',
     'REJECTED'
]

MODEL_ADMISSION_STATUS = configure_options(ADMISSION_STATUS_OPTIONS)


SESSION_OPTIONS=[

]

STANDARDS = [
     0,1,2,3,4,5,11,12,13,14,15
]

FEE_STRUCTURE = {
             0:{
               'Tution Fee':100,
               'Exam Fee':50,
               'Admission Fee':100
               },
             1:{
               'Tution Fee':100,
               'Exam Fee':50,
               'Admission Fee':100
               },
             2:{
               'Tution Fee':100,
               'Exam Fee':50,
               'Admission Fee':100
               },
             3:{
               'Tution Fee':100,
               'Exam Fee':50,
               'Admission Fee':100
               },
             4:{
               'Tution Fee':100,
               'Exam Fee':50,
               'Admission Fee':100
               },
             5:{
               'Tution Fee':100,
               'Exam Fee':50,
               'Admission Fee':100
               },
              6:{
               'Tution Fee':100,
               'Exam Fee':50,
               'Admission Fee':100
               },
              7:{
               'Tution Fee':100,
               'Exam Fee':50,
               'Admission Fee':100
               },
               
               11:{
               'Tution Fee':15000,
               'Exam Fee':1000,
               'Admission Fee':1000
               },
               12:{
               'Tution Fee':16500,
               'Exam Fee':50,
               'Admission Fee':100
               },
               13:{
               'Tution Fee':18000,
               'Exam Fee':50,
               'Admission Fee':100
               },
               14:{
               'Tution Fee':19000,
               'Exam Fee':50,
               'Admission Fee':100
               },
               15:{
               'Tution Fee':20000,
               'Exam Fee':50,
               'Admission Fee':100
               },
                   
              
 
}

RESULTS_SESSION = True

ADMISSIONS_SESSION = True

GOOGLE_SPREADSHEET_NAME = 'database'

CREDENTIALS_PATH = os.path.join(BASE_DIR,'DataProcessorSystem/GoogleSheetProcessor/credentials.json')



#DATABASE_CONFIGURATIONS
#If True the mention the password 
#and username along with IpAddress
DATABASE_CONFIG = False


#Fee Reminder Message
#Title of Fee Reminder
FEE_TITLE='FEE TITLE'
#Fee Message of the school
FEE_MESSAGE = 'FEE MESSAGE'

#Animation File path
#Animation Graphics Path
#Files Related Concepts


STANDARD_STRENGTH_ANIMATIONS ={

  'BAR_GRAPH':'DataProcessorSystem/StaticDataProcessor/designs/Animations/StandardStrength/bar_graph.png',
  
  'PIE_GRAPH':'DataProcessorSystem/StaticDataProcessor/designs/Animations/StandardStrength/pie_digram.png',
  
}

MANAGER_RESULTS_ANIMATIONS ={

  'BAR_GRAPH':'DataProcessorSystem/StaticDataProcessor/designs/Animations/ManagerResults/bar_graph.png',
  
  'PIE_DIGRAM':'DataProcessorSystem/StaticDataProcessor/designs/Animations/ManagerResults/pie_digram.png',
  
}


MESSAGES_VIEWED_ANIMATIONS ={

  'BAR_GRAPH':'DataProcessorSystem/StaticDataProcessor/designs/Animations/MessageViewed/bar_graph.png',
  
  'PIE_DIGRAM':'DataProcessorSystem/StaticDataProcessor/designs/Animations/MessageViewed/pie_digram.png',
  
}


LOGIN_PASSWORD = 'hari'


UPLOAD_DOCUMENTS = 'DataProcessorSystem/StaticDataProcessor/uploads/documents/'

UPLOAD_POSTURES = 'DataProcessorSystem/StaticDataProcessor/uploads/postures/'

UPLOAD_PROFILE = 'DataProcessorSystem/StaticDataProcessor/uploads/profiles/'




