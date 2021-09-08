from django.contrib import admin

from mysite.coresettings.appconf import Management as Management_app

from Applications.Management.models import (
        Management,
        Event,
        EventRegister,
        Player,
        SchoolTeam,
        Report
        )

if Management_app.db_read or Management_app.db_write:
	admin.site.register(Event)
	admin.site.register(EventRegister)
	admin.site.register(Management)
	admin.site.register(Player)
	admin.site.register(SchoolTeam)
	admin.site.register(Report)            




