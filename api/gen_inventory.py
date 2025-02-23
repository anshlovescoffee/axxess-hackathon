import pandas as pd
import numpy as np

inventory = pd.DataFrame({
    "item": [
        "wheelchair", "bandages", "syringes", "insulin", "antibiotics", "scalpel", "crutches", "ibuprofen", "gauze",
        "paracetamol", "oxygen tank", "stethoscope", "gloves", "face mask", "morphine", "saline solution", "defibrillator",
        "thermometer", "epinephrine", "amoxicillin", "blood pressure monitor", "antiseptic wipes", "cotton swabs", "eye drops",
        "hydrocortisone cream", "lancets", "test strips", "betadine", "fentanyl patch"
    ],
    "quantity_unit": [
        "each", "box", "each", "vial", "pill", "each", "pair", "mg", "roll",
        "mg", "each", "each", "box", "box", "mg", "liter", "each",
        "each", "mg", "pill", "each", "box", "box", "bottle",
        "tube", "box", "box", "bottle", "patch"
    ],
    "quantity": [
        10, 100, 200, 30, 500, 15, 25, 1000, 75,
        500, 5, 12, 500, 300, 100, 20, 3,
        50, 30, 600, 8, 250, 1000, 50,
        40, 500, 200, 100, 20
    ],
    "restock_threshold": [
        5, 50, 100, 10, 200, 5, 10, 500, 30,
        200, 2, 5, 200, 100, 50, 5, 1,
        10, 10, 300, 2, 100, 400, 20,
        15, 250, 100, 50, 5
    ]
})
inventory.set_index(inventory['item'])
inventory.to_csv('sample_data.csv', index=False)
