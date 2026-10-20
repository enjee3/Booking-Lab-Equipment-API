from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Equipment

app = FastAPI(title="Lab Equipment Booking API")

# Give each request a database session.
DbSession = Annotated[Session, Depends(get_db)]


# Validate incoming equipment details.
class EquipmentCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: str = Field(min_length=1, max_length=100)
    location: str = Field(min_length=1, max_length=100)


class EquipmentUpdate(EquipmentCreate):
    is_active: bool


# Define the equipment information returned by the API.
class EquipmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    location: str
    is_active: bool


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/equipment", response_model=list[EquipmentRead])
def list_equipment(db: DbSession):
    statement = select(Equipment).order_by(Equipment.id)
    return db.scalars(statement).all()


@app.get("/equipment/{equipment_id}", response_model=EquipmentRead)
def get_equipment(equipment_id: int, db: DbSession):
    item = db.get(Equipment, equipment_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found",
        )

    return item


@app.post("/equipment", response_model=EquipmentRead, status_code=201)
def create_equipment(data: EquipmentCreate, db: DbSession):
    item = Equipment(
        name=data.name,
        location=data.location,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@app.put("/equipment/{equipment_id}", response_model=EquipmentRead)
def update_equipment(
    equipment_id: int,
    data: EquipmentUpdate,
    db: DbSession,
):
    # Lock this row while updating it.
    item = db.get(Equipment, equipment_id, with_for_update=True)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found",
        )

    item.name = data.name
    item.location = data.location
    item.is_active = data.is_active

    db.commit()
    db.refresh(item)

    return item