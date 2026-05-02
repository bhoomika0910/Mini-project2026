import json
from pathlib import Path

from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import get_db, Reading, engine, Base

try:
    import joblib
except ImportError:
    joblib = None

# Create tables in Render
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Load AI models at startup
rf_model = joblib.load("ai_models/rf_model.pkl") if joblib else None
iso_model = joblib.load("ai_models/iso_model.pkl") if joblib else None

RISK_LABELS = {0: "Low", 1: "Medium", 2: "High"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(connection)


manager = ConnectionManager()

MODEL_DIR = Path(__file__).resolve().parent.parent / "ai_models"
RF_MODEL_PATH = MODEL_DIR / "rf_model.pkl"
ISO_MODEL_PATH = MODEL_DIR / "iso_model.pkl"

rf_model = joblib.load(RF_MODEL_PATH) if joblib and RF_MODEL_PATH.exists() else None
iso_model = joblib.load(ISO_MODEL_PATH) if joblib and ISO_MODEL_PATH.exists() else None


class SensorDataRequest(BaseModel):
    monument: str
    timestamp: str
    temperature: float
    humidity: float
    air_pollution: float
    vibration: float
    crack_width: float


def calculate_shi(risk_level: int, anomaly: int, temp: float, aqi: float) -> float:
    # Base health out of 100%
    base_score = 100.0 - (risk_level * 20.0) 
    
    # Real-time fluctuation based on live environment
    penalty = (temp * 0.15) + (aqi * 0.02)
    
    final_shi = base_score - penalty
    if anomaly == -1:
        final_shi -= 15.0
        
    return round(max(0.0, final_shi), 2)


def calculate_ai_metrics(data: SensorDataRequest):
    features = [[
        data.temperature,
        data.humidity,
        data.air_pollution,
        data.vibration,
        data.crack_width,
    ]]

    if rf_model is not None:
        risk_level = int(rf_model.predict(features)[0])
    else:
        # REALISTIC THRESHOLDS FOR HERITAGE MONUMENTS
        # High Risk: Fire, Earthquake, Severe Structural Failure, Extreme Pollution
        if (
            data.temperature > 50 
            or data.air_pollution > 600 
            or data.vibration > 5.0 
            or data.crack_width > 2.5
        ):
            risk_level = 2
        # Medium Risk: Extreme Weather, High Traffic Vibrations, Smog Alert
        elif (
            data.temperature > 45 
            or data.air_pollution > 400 
            or data.vibration > 1.5 
            or data.crack_width > 1.0
        ):
            risk_level = 1
        # Low Risk: Normal Environmental Conditions
        else:
            risk_level = 0

    if iso_model is not None:
        anomaly = int(iso_model.predict(features)[0])
    else:
        anomaly = -1 if risk_level == 2 else 1

    shi = calculate_shi(risk_level, anomaly, data.temperature, data.air_pollution)
    return shi, risk_level, anomaly


def serialize_reading(reading: Reading):
    return {
        "id": reading.id,
        "monument": reading.monument,
        "timestamp": reading.timestamp,
        "temperature": reading.temperature,
        "humidity": reading.humidity,
        "air_pollution": reading.air_pollution,
        "vibration": reading.vibration,
        "crack_width": reading.crack_width,
        "risk_level": reading.risk_level,
        "anomaly": reading.anomaly,
        "shi": reading.shi,
    }


@app.websocket("/ws/live-data")
async def websocket_live_data(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.post("/sensor-data")
async def create_sensor_data(data: SensorDataRequest, db: Session = Depends(get_db)):
    Base.metadata.create_all(bind=engine)
    
    shi, risk_level, anomaly = calculate_ai_metrics(data)
    reading = Reading(
        monument=data.monument,
        timestamp=data.timestamp,
        temperature=data.temperature,
        humidity=data.humidity,
        air_pollution=data.air_pollution,
        vibration=data.vibration,
        crack_width=data.crack_width,
        risk_level=risk_level,
        anomaly=anomaly,
        shi=shi,
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)

    payload = json.dumps(serialize_reading(reading))
    await manager.broadcast(payload)

    return {"status": "ok", "message": "Data saved successfully"}


@app.get("/latest")
def get_latest_readings(db: Session = Depends(get_db)):
    from sqlalchemy import func
    
    subquery = (
        db.query(Reading.monument, func.max(Reading.id).label("max_id"))
        .group_by(Reading.monument)
        .subquery()
    )
    
    readings = (
        db.query(Reading)
        .join(subquery, Reading.id == subquery.c.max_id)
        .all()
    )
    
    return [serialize_reading(r) for r in readings]


@app.get("/readings/{monument}")
def get_monument_readings(monument: str, db: Session = Depends(get_db)):
    readings = (
        db.query(Reading)
        .filter(Reading.monument == monument)
        .order_by(Reading.id.desc())
        .limit(50)
        .all()
    )
    
    return [serialize_reading(r) for r in readings]