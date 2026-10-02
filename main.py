from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from models import ConditionEnum, PatientCreate, PatientUpdate, Patient
from database import create_db_and_tables, get_session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/patients", response_model=Patient)
def create_patient(patient_data: PatientCreate, session: Session = Depends(get_session)):
    existing = session.exec(
        select(Patient).where(Patient.medical_record == patient_data.medical_record)
    ).first()

    if existing is not None:
        raise HTTPException(status_code=400, detail="Prontuário já cadastrado")

    patient = Patient(
        name=patient_data.name,
        medical_record=patient_data.medical_record,
        condition=patient_data.condition,
    )
    session.add(patient)
    session.commit()
    session.refresh(patient)

    return patient


@app.get("/patients", response_model=list[Patient])
def list_patients(skip: int = 0, limit: int = 10, condition: ConditionEnum | None = None, session: Session = Depends(get_session)):
    query = select(Patient)

    if condition is not None:
        query = query.where(Patient.condition == condition)

    query = query.offset(skip).limit(limit)

    return session.exec(query).all()


@app.get("/patients/{id}", response_model=Patient)
def get_patient(id: int, session: Session = Depends(get_session)):
    patient = session.get(Patient, id)

    if patient is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    return patient

@app.put("/patients/{id}", response_model=Patient)
def update_patient(id: int, updated_patient: PatientUpdate, session: Session = Depends(get_session)):
    patient = session.get(Patient, id)

    if patient is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    patient.name = updated_patient.name
    patient.medical_record = updated_patient.medical_record
    patient.condition = updated_patient.condition

    session.add(patient)
    session.commit()
    session.refresh(patient)

    return patient


@app.delete("/patients/{id}")
def delete_patient(id: int, session: Session = Depends(get_session)):
    patient = session.get(Patient, id)

    if patient is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    session.delete(patient)
    session.commit()

    return {"Message": "Paciente excluído com sucesso"}


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    fields = []
    for error in exc.errors():
        fields.append({
            "field": error["loc"][-1],
            "message": error["msg"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Um ou mais campos estão inválidos",
                "fields": fields
            }
        }
    )


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail
            }
        }
    )