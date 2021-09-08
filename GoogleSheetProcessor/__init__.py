


class MarkDataBase:
	
	
		
	def setup(self):
		if self.credentials_path and self.sheetname:
			return DataBaseModel(self.sheetname,self.credentials_path)
		else:
			return DataBaseModel('database','credentials.json')
			
	def server_setup(self):
	    from DataProcessorSystem.GoogleSheetProcessor.DataBaseModel import  DataBaseModel
	    from mysite.siteconf import (
		GOOGLE_SPREADSHEET_NAME,
		CREDENTIALS_PATH
		)
	    return DataBaseModel(GOOGLE_SPREADSHEET_NAME,CREDENTIALS_PATH)
		
	def terminal_setup(self):
	    from DataBaseModel import  DataBaseModel as DataBaseModel
	    return DataBaseModel('database','credentials.json') 
			

if __name__=='__main__':
	print('in main funv....')
	mt = MarkDataBase()
	print('installing')
	db = mt.terminal_setup()
	print(db.getAttributes()[3:])
	print(list(db.DataBaseData.sum())[1:-2])
else:
	server = MarkDataBase()
	server_db = server.server_setup()
	server_db.setprimarykey('ID')

