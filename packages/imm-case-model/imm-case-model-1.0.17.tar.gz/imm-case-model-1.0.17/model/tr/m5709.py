from termcolor import colored
from functools import reduce
from typing import List,Optional
from model.common.address import Address
from model.common.phone import Phone
from model.common.trperson import COR, PersonId,Personal,Marriage,Education,Employment,Travel,Family
from model.common.tr import TrCaseIn,TrBackground, SpInCanada
from model.common.commonmodel import CommonModel


class M5709Model(CommonModel):
    personal:Personal
    marriage:Marriage
    personid:List[PersonId]
    address:List[Address]
    education:List[Education]
    employment:List[Employment]
    travel:List[Travel]
    family:List[Family]
    phone:List[Phone]
    cor:List[COR]
    trcase:TrCaseIn
    spincanada:SpInCanada
    trbackground:TrBackground
    
    # initialize the model with a list of excels, which includes all nececcery information the model required. if outpuot_excel_file is not None, it will make an excel file.
    def __init__(self,excels=None,output_excel_file=None):
        if output_excel_file:
            import os
            path=os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
            excels=[
                path+'/template/excel/tr.xlsx',
                path+'/template/excel/pa.xlsx'
            ]
        else:
            if excels is None and len(excels)==0:
                raise ValueError('You must input excel file list as source data for validation')
        super().__init__(excels,output_excel_file,globals())

