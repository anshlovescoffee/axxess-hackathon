from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from typing import List, Optional

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DataFrame with your medical inventory
df = pd.DataFrame({
    "id": range(1, 30),
    "name": [
        "wheelchair", "bandages", "syringes", "insulin", "antibiotics", "scalpel", "crutches", "ibuprofen", "gauze",
        "paracetamol", "oxygen tank", "stethoscope", "gloves", "face mask", "morphine", "saline solution", "defibrillator",
        "thermometer", "epinephrine", "amoxicillin", "blood pressure monitor", "antiseptic wipes", "cotton swabs", "eye drops",
        "hydrocortisone cream", "lancets", "test strips", "betadine", "fentanyl patch"
    ],
    "quantity": [
        10, 4, 100, 30, 20, 3, 25, 6, 24,
        500, 2, 2, 203, 300, 100, 20, 3,
        17, 7, 522, 8, 150, 299, 50,
        40, 50, 143, 50, 20
    ],
    "defaultQuantity": [
        20, 100, 200, 50, 400, 10, 50, 1000, 50,
        1000, 5, 5, 500, 500, 200, 50, 5,
        30, 20, 1000, 15, 300, 500, 100,
        100, 500, 300, 100, 50
    ]
})

class InventoryItem(BaseModel):
    name: str
    quantity: int
    defaultQuantity: Optional[int] = None

@app.get("/api/inventory")
async def get_inventory():
    return df.to_dict(orient="records")

@app.post("/api/inventory")
async def add_inventory_item(item: InventoryItem):
    global df
    
    # Check if item exists
    existing_item = df[df['name'].str.lower() == item.name.lower()]
    
    if not existing_item.empty:
        # Update existing item
        df.loc[df['name'].str.lower() == item.name.lower(), 'quantity'] += item.quantity
    else:
        # Add new item
        new_id = df['id'].max() + 1
        new_row = pd.DataFrame([{
            'id': new_id,
            'name': item.name,
            'quantity': item.quantity,
            'defaultQuantity': item.defaultQuantity or item.quantity * 2  # Default to 2x quantity if not specified
        }])
        df = pd.concat([df, new_row], ignore_index=True)
    
    return {"message": "Item added successfully"}

@app.get("/api/inventory/search")
async def search_inventory(query: str = ""):
    filtered_df = df[df['name'].str.lower().str.contains(query.lower())]
    return filtered_df.to_dict(orient="records")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)