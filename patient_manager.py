import json
import os

PATIENT_FILE = "patients.json"


# =====================================================
# LOAD ONLY PATIENT IDS (for dropdown)
# =====================================================
def load_patients():
    """Return list of patient IDs"""

    if not os.path.exists(PATIENT_FILE):
        return []

    patients = []

    with open(PATIENT_FILE, "r") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                patients.append(data["patient_id"])
            except:
                continue

    return patients


# =====================================================
# REGISTER NEW PATIENT
# =====================================================
def register_patient(patient_data):
    """Save new patient record"""

    # prevent duplicate patient id
    existing = load_all_patient_details()

    for p in existing:
        if p["patient_id"] == patient_data["patient_id"]:
            return False  # already exists

    with open(PATIENT_FILE, "a") as f:
        f.write(json.dumps(patient_data) + "\n")

    return True


# =====================================================
# LOAD FULL PATIENT DETAILS
# =====================================================
def load_all_patient_details():
    """Return complete patient records"""

    if not os.path.exists(PATIENT_FILE):
        return []

    patients = []

    with open(PATIENT_FILE, "r") as f:
        for line in f:
            try:
                patients.append(json.loads(line.strip()))
            except:
                continue

    return patients


# =====================================================
# GET SINGLE PATIENT PROFILE
# =====================================================
def get_patient_details(patient_id):
    """Return one patient's info"""

    patients = load_all_patient_details()

    for p in patients:
        if p["patient_id"] == patient_id:
            return p

    return None