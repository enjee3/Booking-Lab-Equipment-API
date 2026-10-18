from fastapi import FastAPI, HTTPException

app = FastAPI(title="Lab Equipment Booking API")


@app.get("/health")
def health_check():
    return {"status": "ok"}

equipment = [
    {
        "id": 1,
        "name": "Microscope",
        "location": "Lab A",
        "is_active": True,
    },
    {
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