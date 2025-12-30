from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
import json
from typing import Annotated, Literal, Optional

app = FastAPI()


class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the person', examples=['P001'])]
    name: Annotated[str, Field(..., max_length=35, description='Enter name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., description='Enter age of the patient', gt=0, lt=120)]
    gender: Annotated[Literal['male', 'female'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='height of the patient in meters')]
    weight: Annotated[float, Field(..., gt=0, description='weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        return (self.weight)/(self.height **2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi<18.5:
            return 'Underweight'
        elif 18.5<self.bmi<24.9:
            return 'Normal'
        elif 25<self.bmi<29.9:
            return 'Overweight'
        else:
            return 'Obese'
        

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(gt=0, default=None)]
    weight: Annotated[Optional[float], Field(gt=0, default=None)]



def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data


def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)


@app.get("/")
def hello():
    return {"message": "Patient Management system api"}

@app.get("/about")
def hello1():
    return {"message": "A Fully functional API to manage  your patient records"}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="ID of the patient in the DB", example='P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')


@app.get('/sort')
def sort_patients(sort_by:str = Query(..., description='Sort on the basis of height, weight and bmi'), order : str = Query('asc', description='sort  in asc or desc order')):
    
    valid_fields = ['height','weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Ivalid fields select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail=f'Ivalid order select between asc or desc')
    
    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data



@app.post('/create')
def create_patient(patient: Patient):
    #load existing data
    data = load_data()

    #check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient details already exists')

    #add new patient
    data[patient.id] = patient.model_dump(exclude={'id'})

    #save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient details created successfully'})



@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    # existing_pytient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydantic_object = Patient(**existing_patient_info)
    # pydantic object -> dict
    patient_pydantic_object.model_dump(exclude={'id'})

    data[patient_id] = existing_patient_info
    
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient details updated successfully'})



@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient details deleted successfully'})