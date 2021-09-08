from django.contrib import admin

from Applications.DashBoard.models import (
          Notification,
          Circular,
          Reminder,
          GroupChat,
          Chat,
          IndividualMessage,
          
          )
from mysite.coresettings.appconf import DashBoard

if DashBoard.db_read or DashBoard.db_write:
	admin.site.register(Notification)
	admin.site.register(Reminder)
	admin.site.register(Circular)
	admin.site.register(GroupChat)
	admin.site.register(Chat)
	admin.site.register(IndividualMessage)
	