# before '_' is sheet name
# variable as key, xpath of xml as value. 
data_model={
    'applicant':{
        "name":"page1/SectionA/Applicant/AppName",
        "marital_status":"page1/SectionA/Applicant/ChildMStatus",	
        "date_of_birth":"page1/SectionA/Applicant/AppDOB",	
        "birth_country":"page1/SectionA/Applicant/AppCOB",	
        "address":"page1/SectionA/Applicant/AppAddress",
        "occupation":"page1/SectionA/Applicant/AppOccupation"
    },
    'spouse':{
        "name":"page1/SectionA/Spouse/SpouseName",
        "marital_status":"page1/SectionA/Spouse/ChildMStatus",	
        "date_of_birth":"page1/SectionA/Spouse/SpouseDOB",	
        "birth_country":"page1/SectionA/Spouse/SpouseCOB",	
        "address":"page1/SectionA/Spouse/SpouseAddress",
        "occupation":"page1/SectionA/Spouse/SpouseOccupation",	
        "accompany_to_canada_yes":"page1/SectionA/Spouse/SpouseYes",
        "accompany_to_canada_no":"page1/SectionA/Spouse/SpouseNo"
    },
    'mother':{
        "name":"page1/SectionA/Mother/MotherName",
        "marital_status":"page1/SectionA/Mother/ChildMStatus",	
        "date_of_birth":"page1/SectionA/Mother/MotherDOB",	
        "birth_country":"page1/SectionA/Mother/MotherCOB",	
        "address":"page1/SectionA/Mother/MotherAddress",
        "occupation":"page1/SectionA/Mother/MotherOccupation",	
        "accompany_to_canada_yes":"page1/SectionA/Mother/MotherYes",
        "accompany_to_canada_no":"page1/SectionA/Mother/MotherNo"
    },
    'father':{
        "name":"page1/SectionA/Father/FatherName",
        "marital_status":"page1/SectionA/Father/ChildMStatus",	
        "date_of_birth":"page1/SectionA/Father/FatherDOB",	
        "birth_country":"page1/SectionA/Father/FatherCOB",	
        "address":"page1/SectionA/Father/FatherAddress",
        "occupation":"page1/SectionA/Father/FatherOccupation",	
        "accompany_to_canada_yes":"page1/SectionA/Father/FatherYes",
        "accompany_to_canada_no":"page1/SectionA/Father/FatherNo"
    },
    'children':{
        "name":"ChildName",
        "marital_status":"ChildMStatus",	
        "relationship":"ChildRelationship",
        "date_of_birth":"ChildDOB",	
        "birth_country":"ChildCOB",	
        "address":"ChildAddress",
        "occupation":"ChildOccupation",	
        "accompany_to_canada_yes":"ChildYes",
        "accompany_to_canada_no":"ChildNo"
    },
    'siblings':{
        "name":"ChildName",
        "marital_status":"ChildMStatus",	
        "relationship":"ChildRelationship",
        "date_of_birth":"ChildDOB",	
        "birth_country":"ChildCOB",	
        "address":"ChildAddress",
        "occupation":"ChildOccupation",	
        "accompany_to_canada_yes":"ChildYes",
        "accompany_to_canada_no":"ChildNo"
    }
}

convert_model={
    'tr_marital_status_pairs':{
            'applicant':['marital_status'],
            'spouse':['marital_status'],
            'mother':['marital_status'],
            'father':['marital_status'],
            'children':['marital_status'],
            'siblings':['marital_status'],
        }
    
}

remove_model={
            'spouse':['accompany_to_canada_yes','accompany_to_canada_no'],
            'mother':['accompany_to_canada_yes','accompany_to_canada_no'],
            'father':['accompany_to_canada_yes','accompany_to_canada_no']
        }