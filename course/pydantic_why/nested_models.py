from pydantic import BaseModel


class Address(BaseModel):
    city: str
    state: str
    pin: str

class Patient(BaseModel):
    name: str
    gender:str
    age: int
    address: Address


address_dict = {'city': 'Kharagpur', 'state': 'West Bengal', 'pin': '721301'}
address1 = Address(**address_dict)

patient_dict = {
    'name': 'Gourav',
    'gender': 'Male',
    'age': 21,
    'address': address1
}
patient1 = Patient(**patient_dict)

def insert_patient_info(patient: Patient):
    print(patient.name)
    print(patient.gender)
    print(patient.age)
    print(patient.address.city, patient.address.state, patient.address.pin)


insert_patient_info(patient1)

temp = patient1.model_dump()
print(temp)
print(type(temp))
temp1 = patient1.model_dump_json()
print(temp1)
print(type(temp1))