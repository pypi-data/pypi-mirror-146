from typing import List
from model.common.commonmodel import CommonModel
from model.recruit.jobaddata import JobOffer,General,ErAddress,ErAddresses
from model.common.wordmaker import WordMaker
import os

class JobadModel(CommonModel):
    general:General
    joboffer:JobOffer
    eraddress:List[ErAddress]
    
    # initialize the model with a list of excels, which includes all nececcery information the model required. if outpuot_excel_file is not None, it will make an excel file.
    def __init__(self,excels=None,output_excel_file=None):
        if output_excel_file:
            path=os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
            excels=[
                path+'/template/excel/er.xlsx'
            ]
        else:
            if excels is None and len(excels)==0:
                raise ValueError('You must input excel file list as source data for validation')
        # call parent class for validating
        super().__init__(excels,output_excel_file,globals())
        
class JobadModelDocxAdapater():
    """This is an adapater to bridging job ad model data and docx data
    """

    def __init__(self,jobad_obj: JobadModel):
        # get original obj, which will be used to generate some value based on it's object methods. 
        # 此处用来处理list里面的一些内容。 
        self.jobad_obj=jobad_obj
        addresses=ErAddresses(self.jobad_obj.eraddress)
        self.jobad_obj.eraddress=addresses.working

    def make(self,output_docx):
        path=os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
        template_path=path+"/template/word/jobad.docx"            
        wm=WordMaker(template_path,self.jobad_obj,output_docx)
        wm.make()

