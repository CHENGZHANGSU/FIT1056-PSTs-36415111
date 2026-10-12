import json, logging

logging.basicConfig(
     level = logging.INFO
     format = 
)

def load_patients():
    try:
        with open("patients.json", "r") as f:
                data = json.load(f)
                return data["patients"]
    except FileNotFoundError:
        raise FileNotFoundError("Patient record not found.")

def update_status(patient_id, status):
    patients = load_patients()
    for p in patients:
        try:
            if p["id"] == patient_id:
                p["status"] = status
        except TypeError:
             raise TypeError("Incorrect type of incoming id or status.")
    with open("patients.json", "w") as f:
        json.dump({"patients":patients}, f)
    print("Update successful!")

def data_type_validation(a, b):
     return type(a) == type(b)
    