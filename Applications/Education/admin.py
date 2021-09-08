from django.contrib import admin

from mysite.coresettings.appconf import (Education)

from Applications.Education.models import (
        Course,
        Content,
        Unit,
        PostAssignment,
        AssignmentDocument,
        PostTutorial,
        )
if Education.db_read or Education.db_write:
	
	admin.site.register(Course)
	admin.site.register(Content)
	admin.site.register(Unit)
	admin.site.register(PostAssignment)
	admin.site.register(AssignmentDocument)
	admin.site.register(PostTutorial)