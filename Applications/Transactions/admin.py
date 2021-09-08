from django.contrib import admin

from mysite.coresettings.appconf import (Transactions)

from Applications.Transactions.models import (
               Transaction,
               TutionFee,
               FeeStructure,
               PaymentCard,
               FeeReminder
               )
if Transactions.db_read or Transactions.db_write:
	
	admin.site.register(Transaction)
	admin.site.register(TutionFee)
	admin.site.register(FeeStructure)
	admin.site.register(PaymentCard)
	admin.site.register(FeeReminder)
	