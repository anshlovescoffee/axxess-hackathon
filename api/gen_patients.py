import pandas as pd
import numpy as np
import string
import random
import hashlib
from datetime import datetime, timedelta

first_names = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", 
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa"
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson"
]

def generate_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_pid(length):
    return ''.join(random.choice(string.digits) for i in range(length))

def generate_height(length):
    return random.randint(135, 200) # Generate random heights from ~4'6 to 6'4

def generate_ssn(length):
    digits = string.digits
    raw = ''.join(random.choice(digits) for i in range(length))

    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

def generate_age():
    return random.randint(80, 105)

def generate_phone():
    area_code = random.randint(100, 999)
    prefix = random.randint(100, 999)
    line_number = random.randint(1000, 9999)
    return f"({area_code}) {prefix}-{line_number}"

street_names = [
    "Main", "Maple", "Oak", "Cedar", "Elm", "Pine", "Washington", "Lake", "Hill", "Sunset",
    "Broadway", "River", "Chestnut", "Park", "Highland", "Walnut", "Spruce", "Adams", "Jefferson"
]

street_types = ["St", "Ave", "Blvd", "Rd", "Ln", "Dr", "Way", "Ct", "Pl"]

cities = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", 
    "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville"
]

states = [
    "NY", "CA", "IL", "TX", "AZ", "PA", "FL", "OH", "GA", "NC", "MI", "WA"
]

def generate_random_address():
    street_number = random.randint(100, 9999)
    street_name = random.choice(street_names)
    street_type = random.choice(street_types)
    city = random.choice(cities)
    state = random.choice(states)
    zip_code = f"{random.randint(10000, 99999)}"
    
    return f"{street_number} {street_name} {street_type}, {city}, {state} {zip_code}", zip_code 

def generate_sex():
    return random.choice([0, 1])

def generate_weight():
    return random.randint(125, 280)

def generate_nurse():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_random_date(start_year=2020, end_year=2025):
    """Generate a random date between start_year and end_year."""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

def generate_heart_rate():
    return random.randint(55, 100)

def generate_bp():
    systolic = random.randint(60, 250)
    diastolic = systolic - random.randint(20, 60)

    return systolic, diastolic

patients = pd.DataFrame()
visits = []

num_rows = 100
string_length = 20
rand_arr = generate_random_address() 

patients = pd.DataFrame({
    'pid': [generate_pid(string_length) for _ in range(num_rows)],
    'ssn': [generate_ssn(10) for _ in range(num_rows)],
    'name': [generate_name() for _ in range(num_rows)],
    'address': [rand_arr[0] for _ in range(num_rows)],
    'zip': [rand_arr[1] for _ in range(num_rows)],
    'age': [generate_age() for _ in range(num_rows)],
    'sex': [generate_sex() for _ in range(num_rows)],
    'weight': [generate_weight() for _ in range(num_rows)],
    'height': [generate_height(3) for _ in range(num_rows)],
    'phone': [generate_phone() for _ in range(num_rows)]
})
patients['dob'] = pd.to_datetime('now') - pd.to_timedelta(patients['age'] * 365, unit='day') - pd.DateOffset(days=random.randint(0, 365))


'''
Visit 

pid
reason
notes
'''

visits_amt = 5 
# Fill visit log for each patient
for i in patients.index:
    log = pd.DataFrame({
        'pid': [patients['pid'][i] for _ in range(visits_amt)],
        'nurse': [generate_nurse() for _ in range(visits_amt)],
        'date': [generate_random_date() for _ in range(visits_amt)],
        'heart_rate': [generate_heart_rate() for _ in range(visits_amt)],
        'reason': [random.choice(["Checkup", "Sick", "Injury", "Other"]) for _ in range(visits_amt)],
        'notes': 'Some notes here',
        'respiratory_rate': [random.randint(12, 20) for _ in range(visits_amt)],
        'temperature': [random.randint(97, 100) for _ in range(visits_amt)],
    })
    for i in log.index: 
        bp = generate_bp()
        log.loc[i, 'bp_systolic'] = bp[0]
        log.loc[i, 'bp_diastolic'] = bp[1]

    visits.append(log)

visits_df = pd.concat(visits)
visits_df.reset_index(inplace=True)
visits_df.sort_values(by='date', inplace=True)
visits_df.set_index('date', inplace=True)
visits_df.drop(columns=['index'], inplace=True)


# Medicine
spec_medications = [
    {"item": "viagra", "quantity_unit": "mg", "quantity": 50, "restock_threshold": 25},
    {"item": "insulin", "quantity_unit": "vial", "quantity": 30, "restock_threshold": 10},
    {"item": "antibiotics", "quantity_unit": "pill", "quantity": 500, "restock_threshold": 200},
    {"item": "ibuprofen", "quantity_unit": "mg", "quantity": 1000, "restock_threshold": 500},
    {"item": "paracetamol", "quantity_unit": "mg", "quantity": 500, "restock_threshold": 200},
    {"item": "morphine", "quantity_unit": "mg", "quantity": 100, "restock_threshold": 50},
    {"item": "epinephrine", "quantity_unit": "mg", "quantity": 30, "restock_threshold": 10},
    {"item": "fentanyl patch", "quantity_unit": "patch", "quantity": 20, "restock_threshold": 5},
    {"item": "hydrocortisone cream", "quantity_unit": "tube", "quantity": 40, "restock_threshold": 15},
    {"item": "eye drops", "quantity_unit": "bottle", "quantity": 50, "restock_threshold": 20},
    {"item": "amoxicillin", "quantity_unit": "pill", "quantity": 600, "restock_threshold": 300},
    {"item": "artificial tears", "quantity_unit": "bottle", "quantity": 40, "restock_threshold": 15},
    {"item": "nasal spray", "quantity_unit": "bottle", "quantity": 60, "restock_threshold": 25}
]
medications = []
for i in spec_medications:
    medications.append(i['item'])

prescriptions = pd.DataFrame({
    'pid': [random.choice(patients['pid']) for _ in range(num_rows)],
    'medication': [random.choice(medications) for _ in range(num_rows)],
    'dosage': [random.randint(1, 3) for _ in range(num_rows)],
    'unit': [random.choice(["pill", "mg", "vial", "patch", "bottle", "tube"]) for _ in range(num_rows)],
    'exp_date': [datetime.now() + timedelta(days=random.randint(365 // 2, 365 * 3), hours=random.randint(1, 24), minutes=random.randint(1, 59)) for _ in range(num_rows)]
})

# prescriptions.to_sql('prescriptions.mdf', index=False)
# patients.to_sql('patients.mdf', index=False)
# visits_df.to_sql('visits.mdf', index=False)

prescriptions.to_csv('prescriptions.csv', index=False)
patients.to_csv('patients.csv', index=False)
visits_df.to_csv('visits.csv', index=False)
