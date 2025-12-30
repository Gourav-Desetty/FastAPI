from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @field_validator('email')    # -----> can be used only in one field
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        # abc@gmail.com
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value
    
    @field_validator('name')        # -----> can be used only in one field
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age>60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact number')
        return model


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print("Inserted into database")

patient_info = {
    'name': 'Gourav',
    'email': 'abc@hdfc.com',
    'age': 75,
    'weight': 75.5,
    'married': False,
    'allergies': ['pollen', 'dust'],
    'contact_details': {
        'phone_no': '65541231897',
        'emergency': '541231678431'
    }
}
patient1 = Patient(**patient_info)
insert_patient_data(patient1)