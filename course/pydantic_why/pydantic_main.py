from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):
    name:Annotated[str, Field(max_length=40, title='Name of the patient', description= 'Give the name of the patient in less than 30 characters', examples=['Gourav', 'Ben'])]
    email: EmailStr
    age:int
    weight: Annotated[float, Field(gt=0, lt=110, strict=True)]
    married: Annotated[bool, Field(default=None, description='Is the patient married or not')]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact_details: Dict[str, str]

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
    'email': 'abc@gmail.com',
    'age': 21,
    'weight': 75.5,
    'married': False,
    # 'allergies': ['pollen', 'dust'],
    'contact_details': {
        'phone_no': '65541231897'
    }
}
patient1 = Patient(**patient_info)
insert_patient_data(patient1)