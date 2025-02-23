import pandas as pd
import numpy as np
import string
import random

patients = pd.DataFrame()

# def generate_random_string(length):
#     letters_and_digits = string.ascii_letters + string.digits
#     return ''.join(random.choice(letters_and_digits) for i in range(length))
#
# def generate_height(length):
#     random.randint(135, 200) # Generate random heights from ~4'6 to 6'4

num_rows = 1000
string_length = 20
patients = pd.DataFrame({
    'patient_id': [generate_random_string(string_length) for _ in range(num_rows)],
    ''
})

print(patients)
