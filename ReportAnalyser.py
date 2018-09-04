import cast.analysers.ua
from cast.analysers import log as Print, CustomObject
import binascii
import os
from os import listdir
from os import walk
import csv

class ReportExtension(cast.analysers.ua.Extension):
    
    def _init_(self):
        self.filename = ""
        self.name = ""
        self.file = ""    
        self.initial_crc =  None
        self.file_ref=""
        return

    def start_analysis(self):
        pass
       
     
    def start_file(self,file):
        Print.debug("Inside start_file")
        self.file = file
        self.filename = file.get_path()
        self.createGenericreportobject();
        pass
                      

    def saveObject(self,obj_reference,name,obj_type,parent,fullname,guid):
        #Print.debug("Saving Object")
        obj_reference.set_name(name)
        obj_reference.set_type(obj_type)
        obj_reference.set_fullname(fullname)
        obj_reference.set_parent(parent)
        obj_reference.set_guid(guid) 
        pass
    

    def end_analysis(self):        
        pass
    
    def createGenericreportobject(self):
        #ReportModule=CustomObject()
        with open(self.filename, "rb") as binary_file:
            self.file_ref=bytearray(binary_file.read())
            index = self.filename.rfind('\\')
            self.name = self.filename[index+1:]
            if self.filename.endswith(".csv"):
                with open(self.filename) as csvfile:
                    readCSV = csv.reader(csvfile)
                    for row in readCSV:
                        ReportModule=CustomObject()
                        self.saveObject(ReportModule,row[0] +"."+ row[1],"GenericReport",self.file,self.filename,"GenericReport_"+row[0] + row[1])
                        ReportModule.save()
            #self.saveObject(ReportModule,self.name,"GenericReport",self.file,self.filename,"GenericReport_"+self.filename)
            #ReportModule.save()
            else:
                ReportModule=CustomObject()
                #Print.debug("Other than CSV file-----------")
                self.saveObject(ReportModule,self.name,"GenericReport",self.file,self.filename,"GenericReport_"+self.filename)
                ReportModule.save()
            checksum = self.getcrc(self.file_ref)
            Print.debug("checksum == "+str(checksum))
            ReportModule.save_property('checksum.CodeOnlyChecksum', checksum)
            Print.debug("End of Analysis!!!") 
            
    def getcrc(self,text, initial_crc = 0):
        return binascii.crc32(text, initial_crc)  - 2**31