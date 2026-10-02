from enum import Enum
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict

class ConditionEnum(str, Enum):
    LM = "LM"
    LEA = "LEA"
    AMPUTADO = "AMPUTADO"
    DNME = "DNME"

CONDITION_LABELS = {
    ConditionEnum.LM: "Lesão Medular",
    ConditionEnum.LEA: "Lesão encefálica adquirida",
    ConditionEnum.AMPUTADO: "Amputado",
    ConditionEnum.DNME: "Doença neuromuscular ou musculoesquelética",
}

class PatientCreate(SQLModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=2)
    medical_record: str = Field(min_length=1)
    condition: ConditionEnum

class PatientUpdate(SQLModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=2)
    medical_record: str = Field(min_length=1)
    condition: ConditionEnum

class Patient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    medical_record: str
    condition: ConditionEnum