from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db, Reading

app = FastAPI()


class SensorDataRequest(BaseModel):
    monument: str
    timestamp: str
    temperature: float
    humidity: float
    air_pollution: float
    vibration: float
    crack_width: float


@app.post("/sensor-data")
def create_sensor_data(data: SensorDataRequest, db: Session = Depends(get_db)):
    reading = Reading(
        monument=data.monument,
        timestamp=data.timestamp,
        temperature=data.temperature,
        humidity=data.humidity,
        air_pollution=data.air_pollution,
        vibration=data.vibration,
        crack_width=data.crack_width,
    )
    db.add(reading)
    db.commit()
    return {"status": "ok", "message": "Data saved successfully"}
