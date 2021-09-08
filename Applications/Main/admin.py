from django.contrib import admin

from mysite.coresettings.appconf import (Main)

from Applications.Main.models import (
         ChannelContent,
         StaffChannelContent,
         LeaveForm
         )



if Main.db_read or Main.db_write:
	
	admin.site.register(ChannelContent)
	admin.site.register(StaffChannelContent)
	admin.site.register(LeaveForm)