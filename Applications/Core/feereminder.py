from Applications.Transactions.models import PaymentCard,Transaction,TutionFee

from Applications.DashBoard.models import IndividualMessage

from Applications.Administration.models import Channel

from mysite.siteconf import FEE_TITLE,FEE_MESSAGE

class FeeReminderSystem:
	
	def __init__(self,month):
		self.month = month
		self.channels = []
		self.pending_tution_fees = []
		
	def get_pending_list(self):
		for tution_fee in TutionFee.objects.filter(month=self.month):
			if tution_fee.paid==False:
				self.pending_tution_fees.append(tution_fee)
		return self.pending_tution_fees
		
		
	def get_channels(self):
		for tution_fee in self.pending_tution_fees:
			self.channels.append(Channel.objects.get(admission_number=tution_fee.reg_number))
		return self.channels
			
	def send_messages(self):
		for channel in self.get_channels():
			self.send_message(channel)
			
			
	def send_message(self,channel):
		IndividualMessage(
		sender=channel,
		title=FEE_TITLE,
		message=FEE_MESSAGE+channel.username
		).send()
		



	
		
		