import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

import pandas as pd

import sys


import os
class DataBaseModel:
    
    def __init__(self,title,credentials_path):
        self.title = title
        self.credentials_path=credentials_path
        
        self.install()
        
    def install(self):
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        
        # Adding Credentials to perform Operations on DataBaseSheet or Google SpreadSheet
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_path, scope)
        
        #self.report.warning(f'@{self.auth_admin}  ADDING CREDENTIALS....')
        
        
        # authorising the client
        self.client = gspread.authorize(self.creds)
        
        self.DataBaseSheet = self.client.open(self.title).sheet1
        
        
        
        
        self.DataBaseData = pd.DataFrame(self.DataBaseSheet.get_all_records())
        
        
        
        
        
        self.DataBase = self.DataBaseSheet.get_all_records()
        '''
        Rank attribute
        '''
        self.rank = len(self.DataBaseData.ID)
        
        self.attributes = None
        
        
        
      

    def verifyattribute(self,key):
        flag=False
        for attire in attribute:
            if attire==key:
                flag=True
        if flag:
            return True
        else:
            return False   
    
    # SETTING ATTRUBUTES.....    
    def setAttributes(self,attributes):
        newattributes=['ID',]
        i=0
        for i in range(len(attributes)):
            newattributes.append(attributes[i])
        self.DataBaseSheet.insert_row(newattributes,1)
        
    #------------------------------ 
    # FINDING CELL ....
    def findcell(self,keyperson,attribute):
       
        # FINDING ROW
        row=1
        for key in self.DataBaseData[self.key]:
            row+=1
            if key==keyperson:
                break
            
        # FINDING COLUMN
        
        col =1
        for attire in self.getAttributes():
            if attire == attribute:
                break
            col += 1
        return [row,col]
    #---------------------------
    
          
    def getvalues(self,keyperson,attributes):
        if type(attributes)==type([]):
            pass
        else:
            attributes = [attributes]
        values = []
        for attire in attributes:
            matrix = self.findcell(keyperson,attire)
            value = self.DataBaseSheet.cell(matrix[0],matrix[1]).value
            try:
                value = int(value)
            except:
                pass
            values.append(value)
        return values
    #---------------------------
    '''
    func name   : getvalue
    params      : keyperson and attribute
    process     : searches the value of the given keyperson's attribute
    returns     : value in str datatype
    '''    
    def getvalue(self,keyperson,attribute):
        matrix = self.findcell(keyperson,attribute)
        values = self.DataBaseSheet.cell(matrix[0],matrix[1]).value
        return values
            
    #-----------------------------
    # REPLACING THE CELL.....
    def replacecell(self,keyperson,attribute,value):
        cell = self.findcell(keyperson,attribute)
        self.DataBaseSheet.update_cell(cell[0],cell[1],value)
        self.attributes = None
             
          
    #-------------------------------
    def getAttributes(self):
        if self.attributes:
            return self.attributes
        else:
            self.attributes = self.DataBaseSheet.row_values(1)
        return self.attributes
          
    #-------------------------------
   
    def setprimarykey(self,key):
        try:
            self.getAttributes()
            flag = False
            for model in self.attributes:
                if key==model:
                    flag = True
                    break
            if flag:
                self.key = key
                
                return key
            else:
                
                return False
        except:
        	pass
    # ----------------------------- 
    def insert(self,record):
        try:
            self.getAttributes()
            position = len(self.DataBaseData.ID)+2
            
            self.DataBaseSheet.insert_row(record,position)
            record = pd.DataFrame([record],columns=self.attributes)
            record = record.loc[0,:]
            
            
            return True
        except:
            pass
            return False
             
    #----------------------------   
    def insertat(self,record,position):
        try:
            self.getAttributes()
            self.DataBaseSheet.insert_row(record,position)
            
            
            record = pd.DataFrame([record],columns=self.attributes)
            record = record.loc[0,:]
            
            return True
        except:
            pass
            
            return False
             
    #-----------------------------
    def deleteat(self,position):
        try:
            record = self.DataBaseSheet.delete_row(position)
            
            
            
            return True   
        except:
            pass
            return False

             
    #-----------------------------
    def delete(self):
        
        try:
            position = len(self.DataBaseData.ID)+2
            record = self.DataBaseSheet.row_values(position)
            self.DataBaseSheet.delete_row(position)
            record = pd.DataFrame([record],columns=self.attributes)
            
            
            return True   
        except:
            pass
            return False           
                        
                                                
    #-----------------------------  
    def searchby(self,element,attribute):
       
        try:
            self.count = 0
            flag = False
            for model in self.DataBaseData[attribute]:
                if model==element:
                    flag = True
                    break
                self.count += 1
            if flag:
                model = self.DataBaseData.loc[self.count,:]
                
                return model
            else:
                
                return 'No record Found' 
        except:
            
            return 'No Attribute'
            


    def getelements(self,attribute,value):
        try:
            count=0
            models=[]
            for model in self.DataBaseData[attribute]:
                if model==value:
                    models.append(self.DataBaseData.loc[count,:])
                count+=1
            return models 
        except:
            return 'No attribute'  
                    
                              
                    
                                   
    def clearDataBase(self):
        try:
            if input('Enter Admin password.  : ')==self.password:
                for count in range(len(self.DataBaseData.ID)+2):
                    self.DataBaseSheet.delete(count)
            else:
                pass
        except:
           pass
   
   
   
    def countnumber(self):
       return len(self.DataBaseData.ID)
   
    #-----------------------------  
    def posterprint(self):
        '''
        func name : posterprint
        prints the entire database in the form of poster for every set of record in database
        parameters: instance method
        returns None
        checked by Theddu Srihari
        '''
        
        for record in self.DataBase:
            print('-'*40)
            print(self.title)
            print('-'*40)
            for value in record.items():
                print(f'{value[0]:18}: {value[1]:18}')
            print('-'*40)




