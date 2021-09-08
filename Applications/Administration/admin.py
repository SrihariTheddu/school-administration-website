'''
    ADMINISTRATION APPLICATION
'''
from django.contrib import admin

from Applications.Administration.models import ( 
               Channel,
               Standard,
               Department,
               TCForm,
               ChangeMobileNumberForm,
               FeedBack,
               AdmissionForm,
               Appointment,
               Manager,
               )

               
from mysite.coresettings.appconf import (Administration)

if Administration.db_read or Administration.db_write:
	admin.site.register(Channel)
	admin.site.register(Standard)
	admin.site.register(Department)
	admin.site.register(TCForm)
	admin.site.register(ChangeMobileNumberForm)
	admin.site.register(FeedBack)
	admin.site.register(Appointment)
	admin.site.register(AdmissionForm)
	admin.site.register(Manager)
	