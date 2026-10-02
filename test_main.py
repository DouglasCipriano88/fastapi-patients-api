from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_patient():
    response = client.post("/patients", json={
        "name": "Ana",
        "medical_record": "100",
        "condition": "LM"
    })

    assert response.status_code == 200
    assert response.json()["name"] == "Ana"

def test_create_patient_invalid_name():
    response = client.post("/patients", json={
        "name": "A",
        "medical_record": "101",
        "condition": "LM"
    })

    assert response.status_code == 422

def test_create_patient_duplicate_medical_record():
    client.post("/patients", json={
        "name": "Bruno",
        "medical_record": "200",
        "condition": "LEA"
    })

    response = client.post("/patients", json={
        "name": "Outro",
        "medical_record": "200",
        "condition": "AMPUTADO"
    })

    assert response.status_code == 400