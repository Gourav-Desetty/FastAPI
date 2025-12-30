from pydantic import BaseModel, EmailStr, AnyUrl, Field, computed_field
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    height: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = (self.weight) / (self.height**2)
        return bmi


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print(f'BMI: {patient.bmi}')
    print("Inserted into database")

patient_info = {
    'name': 'Gourav',
    'email': 'abc@hdfc.com',
    'age': 75,
    'weight': 75.5,
    'height': 80.5,
    'married': False,
    'allergies': ['pollen', 'dust'],
    'contact_details': {
        'phone_no': '65541231897',
        'emergency': '541231678431'
    }
}
patient1 = Patient(**patient_info)
insert_patient_data(patient1)