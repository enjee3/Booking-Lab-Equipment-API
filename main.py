from threading import Lock

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="Lab Equipment Booking API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


equipment = [{
"id": 1,
"name": "Microscope",
"location": "Lab A",
"is_active": True,
},{
"id": 2,
"name": "Centrifuge",
"location": "Lab B",
"is_active": True,
},
]


@app.get("/equipment")
def list_equipment():
    return equipment


@app.get("/equipment/{equipment_id}")
def get_equipment(equipment_id: int):
    for item in equipment:
        if item["id"] == equipment_id:
            return item

    raise HTTPException(
        status_code=404,
        detail="Equipment not found",
    )


# Validate the name and location sent in a creation request.
class EquipmentCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: str = Field(min_length=1, max_length=100)
    location: str = Field(min_length=1, max_length=100)


# This lock belongs outside the class.
equipment_lock = Lock()


# Assign a new ID, add the equipment, and return its record.
@app.post("/equipment", status_code=201)
def create_equipment(data: EquipmentCreate):
    with equipment_lock:
        new_id = max(
            (item["id"] for item in equipment),
            default=0,
        ) + 1

        new_item = {
            "id": new_id,
            "name": data.name,
            "location": data.location,
            "is_active": True,
        }
        equipment.append(new_item)
    return new_item

class EquipmentUpdate(EquipmentCreate):
    is_active: bool


@app.put("/equipment/{equipment_id}")
def update_equipment(equipment_id: int, data: EquipmentUpdate):
    with equipment_lock:
        for item in equipment:
            if item["id"] == equipment_id:
                item.update(data.model_dump())
                return item.copy()

    raise HTTPException(
        status_code=404,
        detail="Equipment not found",
    )